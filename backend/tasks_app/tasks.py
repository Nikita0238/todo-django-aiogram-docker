from celery import shared_task
from .models import Task
from django.utils import timezone
import os
import requests

@shared_task
def send_due_notifications():
    now = timezone.now()
    due = Task.objects.filter(due_date__lte=now, notified=False)
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    for t in due:
        if t.user and t.user.telegram_id and token:
            chat_id = t.user.telegram_id
            text = f"\U0001F514 Задача '{t.title}' наступила. Срок: {t.due_date.isoformat()}"
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            try:
                requests.post(url, json={'chat_id': chat_id, 'text': text})
                t.notified = True
                t.save()
            except Exception as e:
                print('Failed to notify', e)
