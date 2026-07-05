from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None  # убираем username

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Payment(models.Model):
    PAYMENT_METHODS = (
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    )

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="payments")

    payment_date = models.DateTimeField(auto_now_add=True)

    paid_course = models.ForeignKey(
        "lms.Course",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
    )

    paid_lesson = models.ForeignKey(
        "lms.Lesson",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)

    def __str__(self):
        return f"{self.user} - {self.amount}"

