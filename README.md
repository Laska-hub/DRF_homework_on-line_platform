# DRF Homework — Online Learning Platform (LMS)

## Описание проекта

Backend часть LMS (Learning Management System), разработанная на Django и Django REST Framework.

Проект позволяет управлять:

- пользователями
- курсами
- уроками
- платежами

Каждый курс содержит несколько уроков.

В проекте реализованы:
- регистрация пользователей
- JWT-аутентификация
- разграничение прав доступа
- роли пользователей (обычный пользователь и модератор)
- владельцы курсов и уроков


## Технологии

- Python 3.13+
- Django 6
- Django REST Framework
- djangorestframework-simplejwt (JWT authentication)
- SQLite
- Pillow
- Poetry


## Установка и запуск проекта

### 1. Клонировать репозиторий

```bash
git clone git@github.com:Laska-hub/DRF_homework_on-line_platform.git

cd DRF_homework_on-line_platform
2. Установить зависимости
poetry install

Если проект используется только как менеджер зависимостей:

poetry install --no-root
3. Активировать окружение
poetry shell
4. Выполнить миграции
python manage.py migrate
5. Запустить сервер
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

Для доступа к защищенным endpoint необходимо передавать:

Authorization: Bearer <access_token>
Права доступа

В проекте реализованы DRF permissions.

Обычный пользователь

Может:

создавать свои курсы
создавать свои уроки
просматривать свои объекты
редактировать свои объекты
удалять свои объекты

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

Группа модераторов создается через фикстуру:

python manage.py loaddata users/fixtures/groups.json
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
Payments

Платежи пользователей:

GET /api/payments/
POST /api/payments/
GET /api/payments/{id}/
PUT /api/payments/{id}/
DELETE /api/payments/{id}/
Примеры запросов
Создание курса

POST:

/api/courses/
{
    "title": "Django REST Framework",
    "description": "Course about DRF",
    "preview": null
}
Создание урока

POST:

/api/lessons/
{
    "title": "JWT Authentication",
    "description": "Working with tokens",
    "video_url": "https://youtube.com",
    "course": 1
}
Особенности реализации

В проекте реализовано:

кастомная модель пользователя на основе AbstractBaseUser
JWT authentication через SimpleJWT
ModelViewSet для Course и Lesson
DRF permissions
проверка владельца объектов
проверка принадлежности пользователя к группе moderators
автоматическое заполнение owner через perform_create()
фикстура группы moderators
ForeignKey связь Course → Lesson
API возвращает JSON
Проверка проекта

Проверка Django:

python manage.py check

Проверка миграций:

python manage.py makemigrations

Автор: Olesia Laskovets

DRF homework project — LMS platform