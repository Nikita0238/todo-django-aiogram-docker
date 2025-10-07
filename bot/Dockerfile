FROM python:3.11-slim

WORKDIR /bot

COPY bot/requirements.txt /bot/requirements.txt
RUN pip install --upgrade pip && pip install -r /bot/requirements.txt

COPY bot /bot

CMD ["python", "bot.py"]
