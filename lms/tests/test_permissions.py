from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth.models import Group

from users.models import User
from lms.models import Course


class PermissionTestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email="user@test.com",
            password="testpass123"
        )

        self.moderator = User.objects.create_user(
            email="moderator@test.com",
            password="testpass123"
        )

        moderators_group, _ = Group.objects.get_or_create(
            name="moderators"
        )

        self.moderator.groups.add(
            moderators_group
        )

        self.course = Course.objects.create(
            title="Owner course",
            description="Description",
            price=1000,
            owner=self.user
        )


    def test_user_can_update_own_course(self):

        self.client.force_authenticate(
            user=self.user
        )

        response = self.client.patch(
            f"/api/courses/{self.course.id}/",
            {
                "title": "Changed"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


    def test_user_cannot_update_foreign_course(self):

        another_user = User.objects.create_user(
            email="another@test.com",
            password="testpass123"
        )

        self.client.force_authenticate(
            user=another_user
        )

        response = self.client.patch(
            f"/api/courses/{self.course.id}/",
            {
                "title": "Changed"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )


    def test_moderator_can_update_course(self):

        self.client.force_authenticate(
            user=self.moderator
        )

        response = self.client.patch(
            f"/api/courses/{self.course.id}/",
            {
                "title": "Moderator changed"
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


    def test_moderator_cannot_create_course(self):

        self.client.force_authenticate(
            user=self.moderator
        )

        response = self.client.post(
            "/api/courses/",
            {
                "title": "Moderator course",
                "description": "Test",
                "price": 2000
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
