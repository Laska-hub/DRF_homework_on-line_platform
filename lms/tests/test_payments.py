from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User

from lms.models import (
    Course,
    Payment,
)



class PaymentTestCase(APITestCase):


    def setUp(self):

        self.user = User.objects.create_user(
            email="payment@test.com",
            password="testpass123"
        )


        self.course = Course.objects.create(
            title="Stripe Course",
            description="Payment course",
            price=5000,
            owner=self.user
        )


        self.client.force_authenticate(
            user=self.user
        )



    def test_create_payment(self):

        response = self.client.post(
            "/api/payments/create/",
            {
                "paid_course": self.course.id
            },
            format="json"
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )


        payment = Payment.objects.first()


        self.assertEqual(
            payment.user,
            self.user
        )


        self.assertEqual(
            payment.paid_course,
            self.course
        )


        self.assertEqual(
            payment.amount,
            self.course.price
        )


        self.assertEqual(
            payment.payment_method,
            "card"
        )


        self.assertEqual(
            payment.status,
            "pending"
        )


        self.assertIsNotNone(
            payment.payment_link
        )



    def test_payment_requires_authentication(self):

        self.client.force_authenticate(
            user=None
        )


        response = self.client.post(
            "/api/payments/create/",
            {
                "paid_course": self.course.id
            },
            format="json"
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )



    def test_get_payments(self):

        Payment.objects.create(
            user=self.user,
            paid_course=self.course,
            amount=5000,
            payment_method="cash",
        )


        response = self.client.get(
            "/api/payments/"
        )


        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


        self.assertEqual(
            len(response.data["results"]),
            1
        )
