from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):

    def test_create_user(self):

        user = User.objects.create_user(email="test@test.com", password="testpass123")

        self.assertEqual(user.email, "test@test.com")

        self.assertTrue(user.check_password("testpass123"))

    def test_update_user_profile(self):

        user = User.objects.create_user(email="test@test.com", password="testpass123")

        self.client.force_authenticate(user=user)

        response = self.client.patch(
            f"/api/users/{user.id}/", {"phone": "+79999999999", "city": "Moscow"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users(self):

        user = User.objects.create_user(email="test@test.com", password="testpass123")

        self.client.force_authenticate(user=user)

        response = self.client.get("/api/users/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
