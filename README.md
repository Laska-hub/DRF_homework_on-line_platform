# DRF Homework — Online Learning Platform (LMS)

## Описание проекта

Проект представляет собой backend часть LMS (Learning Management System), разработанную на Django и 
Django REST Framework.

Система позволяет управлять:
- пользователями
- курсами
- уроками

Каждый курс может содержать множество уроков.


## Технологии

- Python 3.12+
- Django 6
- Django REST Framework
- SQLite (по умолчанию)
- Pillow (для работы с изображениями)


## Установка и запуск проекта

### 1. Клонировать репозиторий
```bash
git clone git@github.com:Laska-hub/DRF_homework_on-line_platform.git
cd DRF_homework_on-line_platform

2. Установить зависимости (Poetry)
poetry install

3. Активировать окружение
poetry shell

4. Выполнить миграции
python manage.py migrate

5. Запустить сервер
python manage.py runserver

Основные приложения
users

кастомная модель пользователя
авторизация по email
поля:
email (USERNAME_FIELD)
phone
city
avatar

lms
Содержит основные сущности платформы:

Course

title
description
preview (image)

Lesson
title
description
preview (image)
video_url
связь с Course (ForeignKey)

API endpoints

Courses

GET /api/courses/
POST /api/courses/
GET /api/courses/{id}/
PUT /api/courses/{id}/
DELETE /api/courses/{id}/

Lessons

GET /api/lessons/
POST /api/lessons/
GET /api/lessons/{id}/
PUT /api/lessons/{id}/
DELETE /api/lessons/{id}/

Users

GET /api/users/
POST /api/users/
GET /api/users/{id}/
PUT /api/users/{id}/
DELETE /api/users/{id}/

Примеры запросов

Создание курса

POST /api/courses/
{
  "title": "Django",
  "description": "Django course",
  "preview": null
}
Создание урока

POST /api/lessons/
{
  "title": "Lesson 1",
  "description": "Intro",
  "video_url": "https://youtube.com",
  "course": 1
}
Особенности реализации: 

используется ModelViewSet для Course
GenericAPIView для Lesson
кастомная модель пользователя (AbstractBaseUser)
связи Course → Lesson (One-to-Many)
API возвращает JSON

- Автор

Olesia Laskovets
DRF homework project — LMS platform