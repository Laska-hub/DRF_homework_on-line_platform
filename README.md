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
* API-документация
* асинхронные задачи через Celery
* Redis как брокер сообщений
* периодические задачи через Celery Beat
* PostgreSQL для хранения данных
* Docker и Docker Compose
* Gunicorn для запуска Django-приложения
* Nginx как reverse proxy
* автоматический деплой через GitHub Actions

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
* Gunicorn
* Nginx
* GitHub Actions

---

# Архитектура проекта

Проект работает по следующей схеме:

```text
                    Internet
                       │
                       ▼
                  ┌─────────┐
                  │  Nginx  │
                  │ :80     │
                  └────┬────┘
                       │
                       ▼
               ┌──────────────┐
               │   Gunicorn   │
               │    :8000     │
               └──────┬───────┘
                      │
                      ▼
               ┌──────────────┐
               │    Django    │
               │     API      │
               └──────┬───────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      PostgreSQL    Redis      Celery
                                  │
                                  ▼
                             Celery Beat
```

Nginx принимает внешние HTTP-запросы и передаёт их Django-приложению через Gunicorn.

---

# Docker Compose

Для запуска проекта используются следующие сервисы:

* `web` — Django-приложение + Gunicorn
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

Проверить состояние контейнеров:

```bash
docker compose ps
```

---

# Установка и локальный запуск проекта

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

## 3. Запустить Docker Compose

```bash
docker compose up -d
```

После запуска Django-приложение внутри Docker доступно на:

```text
http://127.0.0.1:8000/
```

API-документация:

```text
http://127.0.0.1:8000/api/docs/
```

---

# Gunicorn

Для запуска Django-приложения используется Gunicorn.

Gunicorn запускается внутри контейнера `web` и слушает:

```text
0.0.0.0:8000
```

Проверить запуск Gunicorn:

```bash
docker compose logs web
```

В логах должно присутствовать:

```text
Starting gunicorn
Listening at: http://0.0.0.0:8000
```

Gunicorn используется вместо встроенного Django development server.

---

# Nginx

Nginx используется как reverse proxy перед Gunicorn.

Схема обработки запроса:

```text
Client
  │
  ▼
Nginx :80
  │
  ▼
Gunicorn :8000
  │
  ▼
Django
```

Nginx принимает внешние HTTP-запросы и передаёт их приложению.

Проверить конфигурацию Nginx:

```bash
sudo nginx -t
```

Перезагрузить Nginx после изменения конфигурации:

```bash
sudo systemctl reload nginx
```

Проверить статус:

```bash
sudo systemctl status nginx --no-pager
```

---

# API Documentation

В проекте используется `drf-spectacular`.

## Swagger

Локально:

```text
http://127.0.0.1:8000/api/docs/
```

На сервере:

```text
http://SERVER_IP/api/docs/
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

# Проверка API

Проверить Swagger через curl:

```bash
curl -I http://127.0.0.1:8000/api/docs/
```

При работающем Django/Gunicorn ожидается:

```text
HTTP/1.1 200 OK
Server: gunicorn
```

При обращении через Nginx:

```bash
curl -I http://SERVER_IP/api/docs/
```

Ожидается:

```text
HTTP/1.1 200 OK
Server: nginx
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

Посмотреть все логи:

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

Следить за логами в реальном времени:

```bash
docker compose logs -f web
```

---

# Остановка проекта

Остановить контейнеры:

```bash
docker compose down
```

Для повторного запуска:

```bash
docker compose up -d
```

Docker volumes с данными PostgreSQL сохраняются после обычного:

```bash
docker compose down
```

---

# PostgreSQL

PostgreSQL используется в качестве основной базы данных проекта.

Данные базы сохраняются в Docker volume:

```text
postgres_data
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

Порт PostgreSQL не публикуется наружу, так как внешний доступ к базе данных не требуется.

---

# Redis

Redis используется как брокер сообщений для Celery.

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

Celery Worker запускается автоматически вместе с Docker Compose.

---

# Celery Beat

Celery Beat используется для запуска периодических задач.

Celery Beat запускается автоматически вместе с Docker Compose.

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

Посмотреть логи:

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

Миграции выполняются автоматически при запуске контейнера `web`.

Для ручного запуска:

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

Запуск тестов:

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

# CI/CD и автоматический деплой

Для автоматического деплоя используется GitHub Actions.

Workflow находится в:

```text
.github/workflows/deploy.yml
```

Workflow запускается при push в ветку:

```text
homework_ci_cd
```

Основные этапы:

1. Checkout репозитория.
2. Копирование проекта на сервер через SCP.
3. Подключение к серверу по SSH.
4. Создание `.env` из GitHub Repository Secrets.
5. Сборка Docker-образов.
6. Запуск контейнеров через Docker Compose.

Схема:

```text
Git push
   │
   ▼
GitHub Actions
   │
   ├── Checkout
   │
   ├── SCP → Server
   │
   └── SSH
        │
        ├── create .env
        │
        └── docker compose up -d --build
                         │
                         ▼
                 Docker containers
```

Для подключения к серверу используются GitHub Repository Secrets:

```text
SERVER_HOST
SERVER_USER
SSH_PRIVATE_KEY
```

Переменные окружения приложения также передаются через GitHub Secrets:

```text
SECRET_KEY
STRIPE_SECRET_KEY
POSTGRES_DB
POSTGRES_HOST
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_PORT
REDIS_URL
```

Файл `.env` создаётся непосредственно на сервере во время деплоя и не хранится в репозитории.

---

# Серверный деплой

На сервере проект размещается в директории:

```text
~/DRF_homework_on-line_platform
```

После успешного деплоя контейнеры можно проверить:

```bash
cd ~/DRF_homework_on-line_platform

docker compose ps
```

Проверить работу Django напрямую через Gunicorn:

```bash
curl -I http://127.0.0.1:8000/api/docs/
```

Проверить работу приложения через Nginx:

```bash
curl -I http://SERVER_IP/api/docs/
```

Ожидаемый результат:

```text
HTTP/1.1 200 OK
Server: nginx
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

# Структура проекта

```text
DRF_homework_on-line_platform
│
├── .github
│   └── workflows
│       └── deploy.yml
│
├── docker-compose.yml
├── Dockerfile
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

# Дополнительные возможности

* кастомная модель пользователя
* JWT authentication
* DRF permissions
* роли пользователей
* группа moderators
* автоматическое заполнение owner
* пагинация
* YouTube validator
* Swagger / OpenAPI документация
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
* Docker volumes
* Gunicorn
* Nginx reverse proxy
* GitHub Actions CI/CD
* автоматический деплой на сервер

---

# Автор

Olesia Laskovets

DRF Homework Project — LMS Platform
