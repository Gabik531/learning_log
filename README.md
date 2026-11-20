# Learning Log

Журнал обучения на Django: темы, записи по датам, регистрация и вход.
У каждого пользователя — только свои данные.

## Локальный запуск

```bash
python3 -m venv ll_env
source ll_env/bin/activate
python -m pip install -r requirements.txt
python manage.py makemigrations learning_logs
python manage.py migrate
python manage.py runserver
```

## Запуск через Docker Compose

1. Создайте файл `.env` рядом с `compose.yaml` (в Git он не попадает).
2. Выполните:

```bash
docker compose up -d --build
docker compose exec web python manage.py createsuperuser
```

### Переменные `.env`

| Переменная | Назначение |
| --- | --- |
| `DJANGO_SECRET_KEY` | секретный ключ Django |
| `DJANGO_DEBUG` | `True` или `False` |
| `DJANGO_ALLOWED_HOSTS` | разрешённые адреса через запятую |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | доверенные источники, например `http://192.168.1.11:20010` |
| `DJANGO_USE_HTTPS` | `True` только за HTTPS |
| `SQLITE_PATH` | путь к базе, в контейнере `/app/data/db.sqlite3` |
| `APP_BIND_IP` | `0.0.0.0`, чтобы приложение было доступно по сети |
| `APP_PORT` | внешний порт проекта |
