from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from lms.models import Course, Subscription


class SubscriptionTestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email="user@test.com",
            password="testpass123"
        )

        self.course_owner = User.objects.create_user(
            email="owner@test.com",
            password="testpass123"
        )

        self.course = Course.objects.create(
            title="Test course",
            description="Description",
            price=1000,
            owner=self.course_owner
        )

        self.client.force_authenticate(
            user=self.user
        )


    def test_add_subscription(self):

        response = self.client.post(
            "/api/subscription/",
            {
                "course_id": self.course.id
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertTrue(
            Subscription.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )


    def test_remove_subscription(self):

        Subscription.objects.create(
            user=self.user,
            course=self.course
        )

        response = self.client.post(
            "/api/subscription/",
            {
                "course_id": self.course.id
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertFalse(
            Subscription.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )
