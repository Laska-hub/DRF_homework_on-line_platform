from django.db import models


class Course(models.Model):
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="courses",
        null=True,
        blank=True,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    title = models.CharField(
        max_length=255
    )

    preview = models.ImageField(
        upload_to="course_previews/",
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):
        return self.title


class Lesson(models.Model):
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="lessons",
        null=True,
        blank=True,
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons"
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    preview = models.ImageField(
        upload_to="lesson_previews/",
        blank=True,
        null=True
    )

    video_url = models.URLField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="subscriptions"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subscriptions"
    )

    class Meta:
        unique_together = (
            "user",
            "course",
        )

    def __str__(self):
        return f"{self.user.email} -> {self.course.title}"


class Payment(models.Model):

    PAYMENT_METHODS = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]

    STATUS_CHOICES = [
        ("created", "Создан"),
        ("pending", "Ожидает оплаты"),
        ("paid", "Оплачен"),
        ("failed", "Ошибка"),
    ]

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="payments"
    )

    payment_date = models.DateTimeField(
        auto_now_add=True
    )

    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="payments"
    )

    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="payments"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="created"
    )

    stripe_product_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    stripe_price_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    stripe_session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    payment_link = models.URLField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user.email} - {self.amount}"
