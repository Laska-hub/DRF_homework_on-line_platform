# DRF Homework — Online Learning Platform (LMS)

## Описание проекта

Backend часть LMS (Learning Management System), разработанная на Django и Django REST Framework.

Проект представляет собой онлайн-платформу для обучения, позволяющую пользователям работать с курсами, уроками, подписками и оплатой курсов.

В проекте реализованы:

* регистрация пользователей
* JWT-аутентификация
* управление профилем пользователя
* роли пользователей
* разграничение прав доступа
* управление курсами
* управление уроками
* подписка на курсы
* оплата курсов через Stripe API
* генерация API документации
* асинхронные задачи через Celery
* Redis как брокер сообщений
* периодические задачи через Celery Beat
* PostgreSQL для хранения данных

---

# Технологии

* Python 3.13+
* Django 6
* Django REST Framework
* PostgreSQL 16
* drf-spectacular
* djangorestframework-simplejwt
* Stripe API
* Celery
* Redis
* django-celery-beat
* Pillow
* Poetry
* pytest
* pytest-django
* coverage
* Docker
* Docker Compose

---

# Docker Compose

Для запуска проекта используются следующие сервисы:

* `web` — Django-приложение
* `db` — PostgreSQL
* `redis` — Redis
* `celery` — Celery Worker
* `celery-beat` — Celery Beat

Все сервисы запускаются одной командой:

```bash
docker compose up
```

Для запуска в фоновом режиме:

```bash
docker compose up -d
```

---

# Установка и запуск проекта

## 1. Клонировать репозиторий

```bash
git clone git@github.com:Laska-hub/DRF_homework_on-line_platform.git

cd DRF_homework_on-line_platform
```

## 2. Создать файл `.env`

Скопировать `.env.example`:

```bash
cp .env.example .env
```

Пример содержимого `.env`:

```env
SECRET_KEY=your_secret_key

STRIPE_SECRET_KEY=your_stripe_secret_key

POSTGRES_DB=lms
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0
```

Для реального использования необходимо указать собственный `SECRET_KEY` и Stripe API key.

Файл `.env` не должен попадать в репозиторий.

---

## 3. Запустить проект

Запустить все сервисы одной командой:

```bash
docker compose up
```

Или в фоновом режиме:

```bash
docker compose up -d
```

После запуска Django будет доступен по адресу:

```text
http://127.0.0.1:8000/
```

---

# Проверка состояния контейнеров

Посмотреть запущенные контейнеры:

```bash
docker compose ps
```

Ожидаются следующие сервисы:

```text
web
db
redis
celery
celery-beat
```

Посмотреть логи:

```bash
docker compose logs
```

Логи конкретного сервиса:

```bash
docker compose logs web
docker compose logs celery
docker compose logs celery-beat
docker compose logs db
docker compose logs redis
```

---

# Остановка проекта

Остановить контейнеры:

```bash
docker compose down
```

Остановка контейнеров не удаляет Docker volumes с данными PostgreSQL и Redis.

Для повторного запуска:

```bash
docker compose up
```

---

# PostgreSQL

PostgreSQL используется в качестве основной базы данных проекта.

Данные базы сохраняются в Docker volume:

```text
postgres_data
```

Проверить volumes:

```bash
docker volume ls
```

PostgreSQL внутри Docker-сети доступен по адресу:

```text
db:5432
```

Переменные подключения:

```env
POSTGRES_DB=lms
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

Порт PostgreSQL не публикуется наружу, так как внешний доступ к базе данных для проекта не требуется.

---

# Redis

Redis используется как брокер сообщений для Celery.

Данные Redis сохраняются в Docker volume:

```text
redis_data
```

Redis внутри Docker-сети доступен по адресу:

```text
redis:6379
```

Переменная подключения:

```env
REDIS_URL=redis://redis:6379/0
```

Порт Redis не публикуется наружу, так как внешнее подключение к Redis не требуется.

---

# Celery

В проекте реализована обработка фоновых задач через Celery.

Используются:

* Redis как брокер сообщений
* Celery Worker для выполнения задач
* Celery Beat для периодических задач
* django-celery-beat для хранения расписания

Celery Worker запускается автоматически вместе с Docker Compose:

```bash
docker compose up
```

Отдельно запускать Celery Worker не требуется.

---

# Celery Beat

Celery Beat используется для запуска периодических задач.

Celery Beat также запускается автоматически:

```bash
docker compose up
```

Используется планировщик:

```python
django_celery_beat.schedulers.DatabaseScheduler
```

---

# Реализованные Celery задачи

## Уведомление подписчиков курса

При обновлении курса запускается фоновая задача:

```python
lms.tasks.send_course_update_email
```

Задача отправляет уведомления пользователям, подписанным на курс.

Email backend:

```python
django.core.mail.backends.console.EmailBackend
```

В учебной версии письма выводятся в консоль контейнера `celery`.

Логи можно посмотреть:

```bash
docker compose logs -f celery
```

---

## Блокировка неактивных пользователей

Добавлена периодическая задача:

```python
lms.tasks.deactivate_inactive_users
```

Задача проверяет пользователей и отключает пользователей, которые долго не проявляли активность.

Расписание:

```text
ежедневно в 00:00
```

---

# Миграции

При запуске контейнера `web` миграции выполняются автоматически:

```bash
python manage.py migrate
```

Команда запуска Django:

```text
bash -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
```

При необходимости выполнить миграции вручную:

```bash
docker compose exec web python manage.py migrate
```

Создать новые миграции:

```bash
docker compose exec web python manage.py makemigrations
```

---

# Создание суперпользователя

Создать администратора:

```bash
docker compose exec web python manage.py createsuperuser
```

После создания администратора доступна Django Admin:

```text
http://127.0.0.1:8000/admin/
```

---

# Аутентификация

Используется JWT-аутентификация через SimpleJWT.

Получение токена:

```text
POST /api/token/
```

Пример запроса:

```json
{
    "email": "test@test.com",
    "password": "password"
}
```

Ответ:

```json
{
    "refresh": "token",
    "access": "token"
}
```

Обновление токена:

```text
POST /api/token/refresh/
```

Для защищённых запросов используется заголовок:

```text
Authorization: Bearer <access_token>
```

---

# Документация API

В проекте используется `drf-spectacular`.

## Swagger

```text
http://127.0.0.1:8000/api/docs/
```

## OpenAPI schema

```text
http://127.0.0.1:8000/api/schema/
```

## ReDoc

```text
http://127.0.0.1:8000/api/redoc/
```

---

# Приложение users

Реализовано:

* кастомная модель пользователя
* регистрация пользователей
* JWT authentication
* управление пользователями
* роли пользователей

Модель пользователя содержит:

* email
* phone
* city
* avatar

Email используется как:

```python
USERNAME_FIELD = "email"
```

---

# Приложение lms

Основные модели:

* Course
* Lesson
* Subscription
* Payment

---

# Course

Курс содержит:

* owner
* title
* description
* preview
* price
* updated_at

Связь:

```text
Course 1 ---- N Lesson
```

При обновлении курса запускается уведомление подписчиков.

---

# Lesson

Урок содержит:

* owner
* course
* title
* description
* preview
* video_url

Для поля `video_url` реализована проверка.

Разрешены только ссылки на YouTube.

---

# Subscription

Подписка пользователя на курс.

Поля:

* user
* course

Связь:

```text
User 1 ---- N Subscription N ---- 1 Course
```

Добавление или удаление подписки выполняется одним запросом.

---

# Payment

Оплата курса через Stripe.

Поля:

* user
* paid_course
* amount
* payment_method
* status
* stripe_product_id
* stripe_price_id
* stripe_session_id
* payment_link

---

# Stripe Integration

Реализован сервисный слой:

```text
lms/services.py
```

Используются:

```python
stripe.Product.create()
```

для создания продукта,

```python
stripe.Price.create()
```

для создания цены,

```python
stripe.checkout.Session.create()
```

для создания Checkout Session.

Пользователю возвращается ссылка на оплату Stripe Checkout.

---

# Права доступа

## Обычный пользователь

Может:

* создавать свои курсы
* создавать свои уроки
* редактировать свои объекты
* удалять свои объекты
* подписываться на курсы
* создавать платежи

Не может:

* изменять чужие объекты

---

## Модератор

Группа:

```text
moderators
```

Может:

* видеть все курсы
* видеть все уроки
* редактировать любые курсы
* редактировать любые уроки

Не может:

* создавать курсы
* создавать уроки
* удалять курсы
* удалять уроки

---

# API Endpoints

## Users

```text
GET    /api/users/
POST   /api/users/
GET    /api/users/{id}/
```

## Courses

```text
GET    /api/courses/
POST   /api/courses/
GET    /api/courses/{id}/
PUT    /api/courses/{id}/
PATCH  /api/courses/{id}/
DELETE /api/courses/{id}/
```

## Lessons

```text
GET    /api/lessons/
POST   /api/lessons/
GET    /api/lessons/{id}/
PUT    /api/lessons/{id}/
PATCH  /api/lessons/{id}/
DELETE /api/lessons/{id}/
```

## Subscription

```text
POST /api/subscription/
```

Пример запроса:

```json
{
    "course_id": 1
}
```

Пример ответа:

```json
{
    "message": "Подписка добавлена"
}
```

---

## Payments

```text
GET  /api/payments/
POST /api/payments/create/
```

---

# Тестирование

В проекте реализованы автоматические тесты:

* users
* courses
* lessons
* permissions
* subscriptions
* payments

Запуск тестов в Docker:

```bash
docker compose exec web pytest
```

Проверка покрытия:

```bash
docker compose exec web coverage run -m pytest
docker compose exec web coverage report
```

---

# Проверка проекта

Проверка Django:

```bash
docker compose exec web python manage.py check
```

Создание миграций:

```bash
docker compose exec web python manage.py makemigrations
```

Применение миграций:

```bash
docker compose exec web python manage.py migrate
```

---

# Структура Docker Compose

```text
DRF_homework_on-line_platform
│
├── docker-compose.yml
├── Dockerfile
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── users
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── permissions.py
│
├── lms
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── services.py
│   ├── permissions.py
│   ├── validators.py
│   ├── tasks.py
│   └── tests
│
└── config
    ├── settings.py
    ├── celery.py
    └── urls.py
```

---

# Docker Volumes

Для сохранности данных используются Docker volumes:

```text
postgres_data
redis_data
static_volume
```

PostgreSQL:

```text
postgres_data:/var/lib/postgresql/data/
```

Redis:

```text
redis_data:/data
```

Static files:

```text
static_volume:/code/static
```

---

# Дополнительные возможности

* кастомная модель пользователя
* JWT authentication
* DRF permissions
* роли пользователей
* группа moderators
* автоматическое заполнение owner
* пагинация
* YouTube validator
* Swagger документация
* Stripe API integration
* сохранение платежных данных
* автоматические тесты
* Celery background tasks
* Redis message broker
* Celery Beat scheduler
* django-celery-beat periodic tasks
* уведомления подписчиков курса
* автоматическая блокировка неактивных пользователей
* Docker Compose
* PostgreSQL
* Docker volumes для сохранения данных

---

# Автор

Olesia Laskovets

DRF Homework Project — LMS Platform
