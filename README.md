# DRF Homework — Online Learning Platform (LMS)

## Описание проекта

Backend часть LMS (Learning Management System), разработанная на Django и Django REST Framework.

Проект позволяет управлять:

- пользователями
- курсами
- уроками
- подписками на курсы

Каждый курс содержит несколько уроков.

В проекте реализованы:

- регистрация пользователей
- JWT-аутентификация
- разграничение прав доступа
- роли пользователей (обычный пользователь и модератор)
- владельцы курсов и уроков
- подписка пользователей на курсы


## Технологии

- Python 3.13+
- Django 6
- Django REST Framework
- djangorestframework-simplejwt
- SQLite
- Pillow
- Poetry
- pytest
- pytest-django
- coverage


# Установка и запуск проекта

## 1. Клонировать репозиторий

```bash
git clone git@github.com:Laska-hub/DRF_homework_on-line_platform.git

cd DRF_homework_on-line_platform
2. Установить зависимости
poetry install

Если проект используется только как менеджер зависимостей:

poetry install --no-root
3. Активировать виртуальное окружение
poetry shell
4. Выполнить миграции
python manage.py migrate
5. Создать группу модераторов

Загрузить фикстуру:

python manage.py loaddata users/fixtures/groups.json
6. Запустить сервер
python manage.py runserver
Структура проекта
users

Приложение пользователей.

Реализовано:

кастомная модель пользователя
авторизация по email
регистрация пользователей
JWT authentication
управление профилем пользователя

Поля пользователя:

email (USERNAME_FIELD)
phone
city
avatar
lms

Основное приложение платформы.

Содержит сущности:

Course
Lesson
Subscription
Course

Поля:

owner
title
description
preview
Lesson

Поля:

owner
course (ForeignKey)
title
description
preview
video_url

Связь:

Course 1 ---- N Lesson
Subscription

Подписка пользователя на курс.

Поля:

user
course

Связь:

User 1 ---- N Subscription N ---- 1 Course
Аутентификация

В проекте используется JWT-аутентификация через SimpleJWT.

Получение токена

POST:

/api/token/

Пример запроса:

{
    "email": "test@test.com",
    "password": "12345"
}

Ответ:

{
    "refresh": "token",
    "access": "token"
}
Обновление токена

POST:

/api/token/refresh/

Для доступа к защищённым endpoint необходимо передавать:

Authorization: Bearer <access_token>
Права доступа
Обычный пользователь

Может:

создавать свои курсы
создавать свои уроки
просматривать свои объекты
редактировать свои объекты
удалять свои объекты
подписываться на курсы

Не может:

работать с чужими объектами
Модератор

Пользователь группы:

moderators

Может:

просматривать все курсы
просматривать все уроки
редактировать любые курсы
редактировать любые уроки

Не может:

создавать курсы
создавать уроки
удалять курсы
удалять уроки
API Endpoints
Users

Получение списка пользователей:

GET /api/users/

Создание пользователя:

POST /api/users/

Получение пользователя:

GET /api/users/{id}/

Обновление пользователя:

PUT /api/users/{id}/

Удаление пользователя:

DELETE /api/users/{id}/
Courses

Получение списка курсов:

GET /api/courses/

Создание курса:

POST /api/courses/

Получение курса:

GET /api/courses/{id}/

Обновление курса:

PUT /api/courses/{id}/

Удаление курса:

DELETE /api/courses/{id}/
Lessons

Получение списка уроков:

GET /api/lessons/

Создание урока:

POST /api/lessons/

Получение урока:

GET /api/lessons/{id}/

Обновление урока:

PUT /api/lessons/{id}/

Удаление урока:

DELETE /api/lessons/{id}/
Subscription

Добавление или удаление подписки на курс:

POST /api/subscription/

Пример запроса:

{
    "course_id": 1
}

Ответ при добавлении:

{
    "message": "Подписка добавлена"
}

Ответ при удалении:

{
    "message": "Подписка удалена"
}
Примеры запросов
Создание курса

POST:

/api/courses/

Запрос:

{
    "title": "Django REST Framework",
    "description": "Course about DRF",
    "preview": null
}
Создание урока

POST:

/api/lessons/

Запрос:

{
    "title": "JWT Authentication",
    "description": "Working with tokens",
    "video_url": "https://youtube.com",
    "course": 1
}
Особенности реализации

В проекте реализовано:

кастомная модель пользователя на основе AbstractUser
авторизация пользователя по email
JWT authentication через SimpleJWT
ModelViewSet для Course и Lesson
DRF permissions
проверка владельца объектов
проверка принадлежности пользователя к группе moderators
автоматическое заполнение owner через perform_create()
фикстура группы moderators
ForeignKey связь Course → Lesson
подписка пользователя на курс
пагинация курсов и уроков
API возвращает JSON
Тестирование

В проекте реализованы автоматические тесты:

users
courses
lessons
permissions
subscriptions

Запуск всех тестов:

poetry run pytest

Проверка покрытия:

poetry run coverage run -m pytest

poetry run coverage report

Текущее покрытие проекта:

95%
Проверка проекта

Проверка Django:

python manage.py check

Проверка миграций:

python manage.py makemigrations

Применение миграций:

python manage.py migrate
Автор

Olesia Laskovets

DRF homework project — LMS platform
