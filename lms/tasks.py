from datetime import timedelta

from celery import shared_task

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

from .models import Subscription


User = get_user_model()


@shared_task
def send_course_update_email(course_id):
    """Рассылка уведомлений подписчикам курса."""

    recipient_list = list(
        Subscription.objects.filter(course_id=course_id)
        .exclude(user__email="")
        .values_list("user__email", flat=True)
        .distinct()
    )

    if not recipient_list:
        return "Нет подписчиков"

    send_mail(
        subject="Обновление курса",
        message="Материалы курса были обновлены.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )

    return f"Письмо отправлено {len(recipient_list)} пользователям"


@shared_task
def deactivate_inactive_users():
    """
    Блокировка пользователей,
    которые не заходили более месяца.
    """

    month_ago = timezone.now() - timedelta(days=30)

    updated_count = (
        User.objects
        .filter(
            last_login__lt=month_ago,
            is_active=True,
        )
        .update(
            is_active=False
        )
    )

    return f"Заблокировано пользователей: {updated_count}"
