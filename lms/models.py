from django.db import models


class Course(models.Model):
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="courses",
        null=True,
        blank=True,
    )

    title = models.CharField(max_length=255)
    preview = models.ImageField(
        upload_to="course_previews/",
        blank=True,
        null=True
    )
    description = models.TextField(
        blank=True,
        null=True
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

    title = models.CharField(max_length=255)

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
