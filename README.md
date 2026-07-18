# DRF Homework — Online Learning Platform (LMS)

## Описание проекта

Backend часть LMS (Learning Management System), разработанная на Django и Django REST Framework.

Проект представляет собой онлайн-платформу для обучения, позволяющую пользователям работать с курсами, уроками, подписками и оплатой курсов.

В проекте реализованы:

- регистрация пользователей
- JWT-аутентификация
- управление профилем пользователя
- роли пользователей
- разграничение прав доступа
- управление курсами
- управление уроками
- подписка на курсы
- оплата курсов через Stripe API
- генерация API документации


---

# Технологии

- Python 3.13+
- Django 6
- Django REST Framework
- drf-spectacular
- djangorestframework-simplejwt
- Stripe API
- SQLite
- Pillow
- Poetry
- pytest
- pytest-django
- coverage


---

# Установка и запуск проекта

## 1. Клонировать репозиторий

```bash
git clone git@github.com:Laska-hub/DRF_homework_on-line_platform.git

cd DRF_homework_on-line_platform
2. Установить зависимости
poetry install

или:

poetry install --no-root
3. Настроить переменные окружения

Создать файл .env:

SECRET_KEY=your_secret_key

STRIPE_SECRET_KEY=your_stripe_secret_key

Stripe ключ можно получить в тестовом режиме:

https://dashboard.stripe.com/test/apikeys

4. Активировать окружение
poetry shell
5. Выполнить миграции
python manage.py migrate
6. Создать группу модераторов

Загрузить фикстуру:

python manage.py loaddata users/fixtures/groups.json
7. Запустить сервер
python manage.py runserver
Документация API

В проекте используется:

drf-spectacular
Swagger UI

Swagger документация доступна:

http://127.0.0.1:8000/api/docs/

OpenAPI schema:

http://127.0.0.1:8000/api/schema/
Структура проекта
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
│   └── tests
│
└── config
    ├── settings.py
    └── urls.py
Приложение users

Реализовано:

кастомная модель пользователя
регистрация пользователей
JWT authentication
управление пользователями

Модель пользователя:

email
phone
city
avatar

Email используется как:

USERNAME_FIELD
Приложение lms

Основные модели:

Course
Lesson
Subscription
Payment
Course

Курс содержит:

Поля:

owner
title
description
preview
price

Связь:

Course 1 ---- N Lesson
Lesson

Поля:

owner
course
title
description
preview
video_url

Для поля video_url реализована проверка:

разрешены только YouTube ссылки
Subscription

Подписка пользователя на курс.

Поля:

user
course

Связь:

User 1 ---- N Subscription N ---- 1 Course

Добавление или удаление подписки выполняется одним запросом.

Payment

Оплата курса через Stripe.

Поля:

user
paid_course
amount
payment_method
status
stripe_product_id
stripe_price_id
stripe_session_id
payment_link

Связь:

User 1 ---- N Payment N ---- 1 Course
Stripe Integration

Реализован сервисный слой:

lms/services.py

В сервисах реализовано:

Создание продукта Stripe

Используется:

stripe.Product.create()
Создание цены Stripe

Используется:

stripe.Price.create()

Цена передается в копейках:

amount * 100
Создание Checkout Session

Используется:

stripe.checkout.Session.create()

В ответ пользователю возвращается:

информация о платеже
ссылка на оплату Stripe Checkout
Аутентификация

Используется JWT через SimpleJWT.

Получение токена:

POST /api/token/

Пример запроса:

{
    "email": "test@test.com",
    "password": "password"
}

Ответ:

{
    "refresh": "token",
    "access": "token"
}

Обновление токена:

POST /api/token/refresh/

Для защищенных запросов:

Authorization: Bearer <access_token>
Права доступа
Обычный пользователь

Может:

создавать свои курсы
создавать свои уроки
редактировать свои объекты
удалять свои объекты
просматривать свои объекты
подписываться на курсы
создавать платежи

Не может:

изменять чужие объекты
Модератор

Группа:

moderators

Может:

видеть все курсы
видеть все уроки
редактировать любые курсы
редактировать любые уроки

Не может:

создавать курсы
создавать уроки
удалять курсы
удалять уроки
API Endpoints
Users

Получение пользователей:

GET /api/users/

Создание пользователя:

POST /api/users/

Получение пользователя:

GET /api/users/{id}/
Courses

Получение курсов:

GET /api/courses/

Создание курса:

POST /api/courses/

Получение курса:

GET /api/courses/{id}/

Обновление:

PUT /api/courses/{id}/

Удаление:

DELETE /api/courses/{id}/
Lessons

Получение уроков:

GET /api/lessons/

Создание урока:

POST /api/lessons/

Получение урока:

GET /api/lessons/{id}/

Обновление:

PUT /api/lessons/{id}/

Удаление:

DELETE /api/lessons/{id}/
Subscription

Добавить или удалить подписку:

POST /api/subscription/

Запрос:

{
    "course_id": 1
}

Ответ:

{
    "message": "Подписка добавлена"
}

или:

{
    "message": "Подписка удалена"
}
Payments

Получение своих платежей:

GET /api/payments/

Получение платежа:

GET /api/payments/{id}/

Создание платежа:

POST /api/payments/create/

Пример:

{
    "paid_course": 1
}

Ответ содержит:

id платежа
сумму
Stripe ID продукта
Stripe ID цены
Stripe Session ID
ссылку на оплату
Тестирование

Реализованы автоматические тесты:

users
courses
lessons
permissions
subscriptions
payments

Запуск:

poetry run pytest

Текущий результат:

20 passed

Проверка покрытия:

poetry run coverage run -m pytest

poetry run coverage report
Проверка проекта

Проверка Django:

python manage.py check

Создание миграций:

python manage.py makemigrations

Применение миграций:

python manage.py migrate
Реализованные дополнительные возможности
кастомная модель пользователя
JWT authentication
DRF permissions
роли пользователей
группа moderators
автоматическое заполнение owner
пагинация
YouTube validator
Swagger документация
Stripe API integration
сохранение платежных данных
автоматические тесты
Автор

Olesia Laskovets

DRF Homework Project — LMS Platform
