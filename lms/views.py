from django.shortcuts import get_object_or_404
from datetime import timedelta
from django.utils import timezone
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    inline_serializer,
)

from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
)

from .models import (
    Course,
    Lesson,
    Subscription,
    Payment,
)

from .paginators import CourseLessonPagination
from .permissions import IsModerator, IsOwner

from .serializers import (
    CourseSerializer,
    LessonSerializer,
    PaymentSerializer,
)

from .services import (
    create_stripe_product,
    create_stripe_price,
    create_checkout_session,
)
from .tasks import send_course_update_email
from datetime import timedelta

from django.utils import timezone


@extend_schema(tags=["Courses"])
class CourseViewSet(ModelViewSet):

    serializer_class = CourseSerializer
    pagination_class = CourseLessonPagination

    queryset = Course.objects.all()

    def get_queryset(self):

        user = self.request.user

        if user.groups.filter(
            name="moderators"
        ).exists():

            return Course.objects.all().order_by(
                "id"
            )

        return Course.objects.filter(
            owner=user
        ).order_by(
            "id"
        )


    def get_permissions(self):

        if self.action in [
            "update",
            "partial_update"
        ]:

            permission_classes = [
                IsAuthenticated,
                IsOwner | IsModerator
            ]

        elif self.action == "destroy":

            permission_classes = [
                IsAuthenticated,
                IsOwner
            ]

        elif self.action == "create":

            permission_classes = [
                IsAuthenticated,
                ~IsModerator
            ]

        else:

            permission_classes = [
                IsAuthenticated
            ]


        return [
            permission()
            for permission in permission_classes
        ]


    def perform_create(self, serializer):

        serializer.save(
            owner=self.request.user
        )

    def perform_update(self, serializer):

        old_updated_at = serializer.instance.updated_at

        course = serializer.save()

        if (
                timezone.now() - old_updated_at
                >= timedelta(hours=4)
        ):
            send_course_update_email.delay(
                course.id
            )


@extend_schema(tags=["Lessons"])
class LessonViewSet(ModelViewSet):

    serializer_class = LessonSerializer
    pagination_class = CourseLessonPagination

    queryset = Lesson.objects.all()


    def get_queryset(self):

        user = self.request.user

        if user.groups.filter(
            name="moderators"
        ).exists():

            return Lesson.objects.all().order_by(
                "id"
            )

        return Lesson.objects.filter(
            owner=user
        ).order_by(
            "id"
        )


    def get_permissions(self):

        if self.action in [
            "update",
            "partial_update"
        ]:

            permission_classes = [
                IsAuthenticated,
                IsOwner | IsModerator
            ]

        elif self.action == "destroy":

            permission_classes = [
                IsAuthenticated,
                IsOwner
            ]

        elif self.action == "create":

            permission_classes = [
                IsAuthenticated,
                ~IsModerator
            ]

        else:

            permission_classes = [
                IsAuthenticated
            ]


        return [
            permission()
            for permission in permission_classes
        ]


    def perform_create(self, serializer):

        serializer.save(
            owner=self.request.user
        )

    def perform_update(self, serializer):

        lesson = serializer.save()

        course = lesson.course

        if (
                timezone.now() - course.updated_at
                >= timedelta(hours=4)
        ):
            send_course_update_email.delay(
                course.id
            )


@extend_schema(
    tags=["Subscriptions"],
    summary="Подписка на курс",
    description=(
        "Добавляет или удаляет подписку "
        "пользователя на курс."
    ),
    request=inline_serializer(
        name="SubscriptionRequest",
        fields={
            "course_id": serializers.IntegerField()
        },
    ),
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name="SubscriptionResponse",
                fields={
                    "message": serializers.CharField()
                },
            )
        )
    },
)
class SubscriptionAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(self, request):

        course_id = request.data.get(
            "course_id"
        )

        course = get_object_or_404(
            Course,
            id=course_id
        )


        subscription = Subscription.objects.filter(
            user=request.user,
            course=course
        )


        if subscription.exists():

            subscription.delete()

            message = "Подписка удалена"

        else:

            Subscription.objects.create(
                user=request.user,
                course=course
            )

            message = "Подписка добавлена"


        return Response(
            {
                "message": message
            }
        )



@extend_schema(
    tags=["Payments"],
    summary="Создание платежа Stripe",
    request=PaymentSerializer,
    responses={
        201: PaymentSerializer
    }
)
class PaymentCreateAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(self, request):

        course_id = request.data.get(
            "paid_course"
        )


        course = get_object_or_404(
            Course,
            id=course_id
        )


        product = create_stripe_product(
            course.title
        )


        price = create_stripe_price(
            product.id,
            course.price
        )


        session = create_checkout_session(
            price.id
        )


        payment = Payment.objects.create(

            user=request.user,

            paid_course=course,

            amount=course.price,

            payment_method="card",

            stripe_product_id=product.id,

            stripe_price_id=price.id,

            stripe_session_id=session.id,

            payment_link=session.url,

            status="pending",
        )


        serializer = PaymentSerializer(
            payment
        )


        return Response(
            serializer.data,
            status=201
        )



@extend_schema(
    tags=["Payments"]
)
class PaymentViewSet(ReadOnlyModelViewSet):

    serializer_class = PaymentSerializer

    permission_classes = [
        IsAuthenticated
    ]

    pagination_class = CourseLessonPagination

    queryset = Payment.objects.all()


    def get_queryset(self):

        return Payment.objects.filter(
            user=self.request.user
        ).order_by(
            "-payment_date"
        )
