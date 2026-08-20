from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):

        self.owner = User.objects.create_user(
            email="owner@test.com", password="testpass123"
        )

        self.user = User.objects.create_user(
            email="user@test.com", password="testpass123"
        )

        self.course = Course.objects.create(
            title="Test course", description="Description", price=1000, owner=self.owner
        )

        self.lesson = Lesson.objects.create(
            title="Test lesson",
            description="Lesson description",
            video_url="https://youtube.com",
            owner=self.owner,
            course=self.course,
        )

        self.client.force_authenticate(user=self.owner)

    def test_create_lesson(self):

        data = {
            "title": "New lesson",
            "description": "New description",
            "video_url": "https://youtube.com/test",
            "course": self.course.id,
        }

        response = self.client.post("/api/lessons/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data["owner"], self.owner.id)

    def test_get_lessons(self):

        response = self.client.get("/api/lessons/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson_owner(self):

        response = self.client.patch(
            f"/api/lessons/{self.lesson.id}/", {"title": "Updated lesson"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson_owner(self):

        response = self.client.delete(f"/api/lessons/{self.lesson.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
