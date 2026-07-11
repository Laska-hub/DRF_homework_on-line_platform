DRF Homework — Online Learning Platform (LMS)

# Описание проекта

Проект представляет собой backend-часть платформы онлайн-обучения (LMS), разработанную на Django + Django REST Framework.

Система позволяет управлять:

пользователями
курсами
уроками
платежами

Реализована REST API архитектура для взаимодействия со SPA-клиентом.

🛠 Технологии

Python 3.12+
Django 6.x
Django REST Framework
Django Filter
SQLite (по умолчанию)
Pillow (для работы с изображениями)

🚀 Установка и запуск проекта

1. Клонировать репозиторий
git clone git@github.com:Laska-hub/DRF_homework_on-line_platform.git
cd DRF_homework_on-line_platform
2. Установить зависимости
poetry install
3. Активировать окружение
poetry shell
4. Выполнить миграции
python manage.py migrate
5. Запустить сервер
python manage.py runserver

📦 Основные приложения

👤 users

Кастомная модель пользователя (AbstractUser), где авторизация происходит по email.
Поля:

email (USERNAME_FIELD)
phone
city
avatar

Также реализована модель:

💳 Payment

Поля:

user (FK → User)
payment_date
paid_course (FK → Course)
paid_lesson (FK → Lesson)
amount
payment_method (cash / transfer)

🎓 lms

Содержит основные образовательные сущности:

Course
title
description
preview (image)
lessons (связанные уроки)
lessons_count (рассчитываемое поле)
Lesson
title
description
preview (image)
video_url
course (FK → Course)

Связь:

Course → Lesson = One-to-Many
🌐 API endpoints
📚 Courses
GET    /api/courses/
POST   /api/courses/
GET    /api/courses/{id}/
PUT    /api/courses/{id}/
DELETE /api/courses/{id}/
📖 Lessons
GET    /api/lessons/
POST   /api/lessons/
GET    /api/lessons/{id}/
PUT    /api/lessons/{id}/
DELETE /api/lessons/{id}/
👤 Users
GET    /api/users/
GET    /api/users/{id}/
PUT    /api/users/{id}/
DELETE /api/users/{id}/
💳 Payments
GET    /api/payments/
POST   /api/payments/
GET    /api/payments/{id}/
PUT    /api/payments/{id}/
DELETE /api/payments/{id}/
Фильтрация Payments:
payment_method
paid_course
paid_lesson
Сортировка:
payment_date (ordering)
🧪 Примеры запросов
📌 Создание курса
POST /api/courses/
{
  "title": "Django",
  "description": "Django course",
  "preview": null
}
📌 Создание урока
POST /api/lessons/
{
  "title": "Lesson 1",
  "description": "Intro",
  "video_url": "https://youtube.com",
  "course": 1
}
📌 Создание платежа
POST /api/payments/
{
  "user": 1,
  "paid_course": 1,
  "paid_lesson": null,
  "amount": "1000.00",
  "payment_method": "cash"
}
⚙️ Особенности реализации
ModelViewSet используется для Course и Payment
Generic-классы используются для Lesson:
ListCreateAPIView
RetrieveUpdateDestroyAPIView
кастомная модель пользователя (email authentication)
Django Filter используется для фильтрации платежей
SerializerMethodField используется для подсчёта уроков курса
nested serializers для отображения уроков внутри курса
связь Course → Lesson (One-to-Many)
👨‍💻 Автор

Olesia Laskovets
DRF homework project — LMS platform