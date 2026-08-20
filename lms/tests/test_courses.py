from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@test.com", password="testpass123"
        )

        self.owner = User.objects.create_user(
            email="owner@test.com", password="testpass123"
        )

        self.course = Course.objects.create(
            title="Test course", description="Description", price=1000, owner=self.owner
        )

        self.client.force_authenticate(user=self.owner)

    def test_create_course(self):

        data = {
            "title": "New course",
            "description": "New description",
            "price": "1500.00",
        }

        response = self.client.post("/api/courses/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data["owner"], self.owner.id)

    def test_get_courses(self):

        response = self.client.get("/api/courses/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data["results"]), 1)

    def test_update_course_owner(self):

        response = self.client.patch(
            f"/api/courses/{self.course.id}/", {"title": "Updated"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["title"], "Updated")

    def test_delete_course_owner(self):

        response = self.client.delete(f"/api/courses/{self.course.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
