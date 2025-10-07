import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import aiohttp
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BACKEND = os.getenv('BACKEND_API_URL', 'http://web:8000/api')
SECRET = os.getenv('BOT_SHARED_SECRET')

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def start_cmd(msg: types.Message):
    await msg.answer('Привет! Я ToDo бот. Используй /tasks для просмотра и /add для добавления.')

@dp.message(Command('tasks'))
async def tasks_cmd(msg: types.Message):
    tg_id = msg.from_user.id
    url = f"{BACKEND}/telegram/{tg_id}/tasks/"
    headers = {'X-BOT-SECRET': SECRET}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                if not data:
                    await msg.answer('У вас нет задач.')
                    return
                lines = []
                for t in data:
                    created = t.get('created_at')
                    cats = ', '.join([c['name'] for c in t.get('categories',[])])
                    lines.append(f"• {t['title']} (создано: {created})\nКатегории: {cats}")
                await msg.answer('\n\n'.join(lines))
            elif resp.status == 404:
                await msg.answer('Вы не зарегистрированы в бэкенде. Попросите администратора зарегистрировать ваш telegram_id.')
            else:
                await msg.answer('Ошибка получения задач.')

@dp.message(Command('add'))
async def add_cmd(msg: types.Message):
    await msg.answer('Отправьте название задачи:')
    try:
        title_msg = await bot.wait_for('message', timeout=120)
        title = title_msg.text.strip()
    except asyncio.TimeoutError:
        await msg.answer('Время ввода истекло.')
        return
    await msg.answer('Отправьте категории через запятую (или пусто):')
    try:
        cats_msg = await bot.wait_for('message', timeout=120)
        cats = [c.strip() for c in cats_msg.text.split(',') if c.strip()]
    except asyncio.TimeoutError:
        await msg.answer('Время ввода истекло.')
        return
    await msg.answer('Отправьте дату в ISO формате (YYYY-MM-DD HH:MM) или пусто:')
    try:
        date_msg = await bot.wait_for('message', timeout=120)
        due = date_msg.text.strip() or None
    except asyncio.TimeoutError:
        await msg.answer('Время ввода истекло.')
        return

    payload = {'title': title, 'description': '', 'category_names': cats}
    if due:
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(due)
            payload['due_date'] = dt.isoformat()
        except Exception:
            await msg.answer('Неверный формат даты. Оставляю без даты.')
    tg_id = msg.from_user.id
    url = f"{BACKEND}/telegram/{tg_id}/tasks/"
    headers = {'X-BOT-SECRET': SECRET, 'Content-Type': 'application/json'}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            if resp.status in (200,201):
                await msg.answer('Задача создана.')
            elif resp.status == 403:
                await msg.answer('Секретный ключ не совпадает. Обратитесь к администратору.')
            else:
                text = await resp.text()
                await msg.answer(f'Ошибка создания: {text}')

if __name__ == '__main__':
    import asyncio
    async def run_bot():
        await dp.start_polling(bot)
    asyncio.run(run_bot())
