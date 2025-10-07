# ToDo Full Project (Django + Aiogram + Celery + Docker)

Important files:

* backend/: Django backend application (users, tasks_app, API)
* bot/: Aiogram Telegram bot with aiogram-dialog
* docker-compose.yml: defines all containers (web, bot, db, redis, celery_worker)
* .env.example: example environment variables for project configuration

Follow steps below to run the project. Open the project folder in PyCharm or your preferred IDE.

## Quick Setup

1. Clone repository:

```bash
git clone https://github.com/Nikita0238/todo-django-aiogram-docker.git
cd todo-django-aiogram-docker
```

2. Copy and configure environment variables:

```bash
cp .env.example .env
# Set TELEGRAM_BOT_TOKEN from BotFather
```

3. Build and start all Docker containers:

```bash
docker-compose up --build
```

Services launched:

* Django API: [http://localhost:8000/](http://localhost:8000/)
* Admin panel: [http://localhost:8000/admin/](http://localhost:8000/admin/)
* Telegram Bot: automatically active after containers start

## Architecture Overview

* **Django Backend**: REST API with CRUD for tasks and categories, Celery for notifications, custom PK generator (no UUID/random/auto-increment), timezone `America/Adak`, admin interface.
* **Aiogram Telegram Bot**: view tasks with categories and creation date, add tasks via dialog, communicates via REST API.
* **Docker Compose**: orchestrates web, bot, db (PostgreSQL), redis (Celery broker), celery_worker (task notifications).

## Features

* Custom PK generator without UUID or random
* REST API integration between bot and Django
* Celery + Redis for asynchronous notifications
* Full Docker integration for easy deployment

## Challenges & Solutions

| Challenge                                      | Solution                                    |
| ---------------------------------------------- | ------------------------------------------- |
| Connect Aiogram bot to Django                  | REST API with BOT_SHARED_SECRET token       |
| Celery worker in Docker                        | Dedicated worker container and Redis broker |
| PK restriction (no UUID/random/auto-increment) | Snowflake-like ID generator                 |
| Timezone handling                              | Set `TIME_ZONE = 'America/Adak'` in Django  |
| Aiogram-dialog integration                     | FSM storage and dialog step handling        |

## Technologies

* Python 3.11
* Django 5 + Django REST Framework
* Aiogram 3 + Aiogram-Dialog
* Celery + Redis
* PostgreSQL
* Docker + Docker Compose

## Author

**Nikita**
GitHub: [https://github.com/Nikita0238](https://github.com/Nikita0238)
