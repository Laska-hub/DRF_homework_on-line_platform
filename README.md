# DRF Homework — Online Learning Platform (LMS)

## Описание проекта

Backend часть LMS (Learning Management System), разработанная на Django и Django REST Framework.

Проект представляет собой онлайн-платформу для обучения, позволяющую пользователям работать с курсами, 
уроками, подписками и оплатой курсов.

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
* очереди задач через Redis
* периодические задачи через Celery Beat


# Технологии

* Python 3.13+
* Django 6
* Django REST Framework
* drf-spectacular
* djangorestframework-simplejwt
* Stripe API
* Celery
* Redis
* django-celery-beat
* SQLite
* Pillow
* Poetry
* pytest
* pytest-django
* coverage

---

# Установка и запуск проекта

## 1. Клонировать репозиторий

```bash
git clone git@github.com:Laska-hub/DRF_homework_on-line_platform.git

cd DRF_homework_on-line_platform
```

## 2. Установить зависимости

```bash
poetry install
```

или:

```bash
poetry install --no-root
```

## 3. Настроить переменные окружения

Создать файл `.env`:

```env
SECRET_KEY=your_secret_key

STRIPE_SECRET_KEY=your_stripe_secret_key

REDIS_URL=redis://127.0.0.1:6379/0
```

Stripe ключ можно получить в тестовом режиме:

https://dashboard.stripe.com/test/apikeys

## 4. Активировать окружение

```bash
poetry shell
```

## 5. Выполнить миграции

```bash
python manage.py migrate
```

## 6. Создать группу модераторов

Загрузить фикстуру:

```bash
python manage.py loaddata users/fixtures/groups.json
```

## 7. Запустить сервер

```bash
python manage.py runserver
```

---

# Celery и фоновые задачи

В проекте реализована обработка фоновых задач через Celery.

Используются:

* Redis как брокер сообщений
* Celery Worker для выполнения задач
* Celery Beat для периодических задач
* django-celery-beat для хранения расписания

## Запуск Celery Worker

Отдельный терминал:

```bash
poetry run celery -A config worker -l info
```

## Запуск Celery Beat

Отдельный терминал:

```bash
poetry run celery -A config beat -l info
```

---

# Реализованные Celery задачи

## Уведомление подписчиков курса

При обновлении курса:

* проверяется время последнего обновления
* если курс не обновлялся более 4 часов
* запускается фоновая задача отправки уведомлений

Task:

```python
lms.tasks.send_course_update_email
```

Получатели берутся из подписок курса.

Email backend:

```python
django.core.mail.backends.console.EmailBackend
```

В учебной версии письма выводятся в консоль.

Пример результата:

```
Subject: Обновление курса

Материалы курса были обновлены.
```

---

## Блокировка неактивных пользователей

Добавлена периодическая задача:

```python
lms.tasks.deactivate_inactive_users
```

Задача:

* проверяет пользователей
* отключает пользователей, которые долго не проявляли активность

Расписание:

ежедневно в 00:00

Используется:

```python
django_celery_beat.schedulers.DatabaseScheduler
```

---

# Документация API

В проекте используется:

* drf-spectacular
* Swagger UI

Swagger документация:

```
http://127.0.0.1:8000/api/docs/
```

OpenAPI schema:

```
http://127.0.0.1:8000/api/schema/
```

---

# Структура проекта

```
DRF_homework_on-line_platform

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

# Приложение users

Реализовано:

* кастомная модель пользователя
* регистрация пользователей
* JWT authentication
* управление пользователями

Модель пользователя:

* email
* phone
* city
* avatar

Email используется как:

```
USERNAME_FIELD
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

Поля:

* owner
* title
* description
* preview
* price
* updated_at

Связь:

```
Course 1 ---- N Lesson
```

При обновлении курса запускается уведомление подписчиков.

---

# Lesson

Поля:

* owner
* course
* title
* description
* preview
* video_url

Для поля `video_url` реализована проверка:

* разрешены только YouTube ссылки

---

# Subscription

Подписка пользователя на курс.

Поля:

* user
* course

Связь:

```
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

```
lms/services.py
```

Используются:

Создание продукта:

```python
stripe.Product.create()
```

Создание цены:

```python
stripe.Price.create()
```

Создание Checkout Session:

```python
stripe.checkout.Session.create()
```

В ответ пользователю возвращается:

* информация о платеже
* ссылка на оплату Stripe Checkout

---

# Аутентификация

Используется JWT через SimpleJWT.

Получение токена:

```
POST /api/token/
```

Пример:

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

Обновление:

```
POST /api/token/refresh/
```

Для защищенных запросов:

```
Authorization: Bearer <access_token>
```

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

```
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

```
GET    /api/users/
POST   /api/users/
GET    /api/users/{id}/
```

## Courses

```
GET    /api/courses/
POST   /api/courses/
GET    /api/courses/{id}/
PUT    /api/courses/{id}/
PATCH  /api/courses/{id}/
DELETE /api/courses/{id}/
```

## Lessons

```
GET    /api/lessons/
POST   /api/lessons/
GET    /api/lessons/{id}/
PUT    /api/lessons/{id}/
PATCH  /api/lessons/{id}/
DELETE /api/lessons/{id}/
```

## Subscription

```
POST /api/subscription/
```

Запрос:

```json
{
    "course_id": 1
}
```

Ответ:

```json
{
    "message": "Подписка добавлена"
}
```

---

## Payments

```
GET  /api/payments/
POST /api/payments/create/
```

---

# Тестирование

Реализованы автоматические тесты:

* users
* courses
* lessons
* permissions
* subscriptions
* payments

Запуск:

```bash
poetry run pytest
```

Результат:

```
20 passed
```

Проверка покрытия:

```bash
poetry run coverage run -m pytest

poetry run coverage report
```

---

# Проверка проекта

Проверка Django:

```bash
python manage.py check
```

Создание миграций:

```bash
python manage.py makemigrations
```

Применение миграций:

```bash
python manage.py migrate
```

---

# Реализованные дополнительные возможности

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

---

# Автор

Olesia Laskovets

DRF Homework Project — LMS Platform
