# Foodgram project

[![Foodgram workflow](https://github.com/Skrapivn/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?event=push)](https://github.com/Skrapivn/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

## Описание проекта

Сайт Foodgram, «Продуктовый помощник». На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Для запуска проекта на локальной машине
Необходимо установить Docker на свою рабочую машину. Инструкцию можно найти на [оффициальном сайте](https://docs.docker.com/get-docker/) по Docker.

После установки Docker необходимо:

1. Клонировать репозиторий:
```bash
git clone https://github.com/Skrapivn/foodgram-project-react.git
```

2. В директории infra/ создайте .env файл в соответствии с `env.example` и укажите значения для переменных окружения:

```python
SECRET_KEY=secretkey  # django секретный ключ
ALLOWED_HOSTS=*  # хост сервера или локальной машины
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```

3. В терминале в папке `infra` запустить **docker-compose**
```
docker-compose up -d
```

5. Выполнить миграции, сборку статических файлов, заполнение базы исходными ингредиентами, создание супер пользователя:

```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --no-input
docker-compose exec backend python manage.py csv_upload
docker-compose exec backend python manage.py createsuperuser
```

#### Автор

[Sergey K.](https://github.com/skrapivn/)
