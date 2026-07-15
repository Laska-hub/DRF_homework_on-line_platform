from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModerator, IsOwner
from .paginators import CourseLessonPagination


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = CourseLessonPagination

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="moderators").exists():
            return Course.objects.all().order_by("id")

        return Course.objects.filter(owner=user).order_by("id")

    def get_permissions(self):

        if self.action in ["update", "partial_update"]:
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


class LessonViewSet(ModelViewSet):
    serializer_class = LessonSerializer
    pagination_class = CourseLessonPagination

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="moderators").exists():
            return Lesson.objects.all().order_by("id")

        return Lesson.objects.filter(owner=user).order_by("id")

    def get_permissions(self):

        if self.action in ["update", "partial_update"]:
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


class SubscriptionAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        user = request.user

        course_id = request.data.get("course_id")

        course = get_object_or_404(
            Course,
            id=course_id
        )

        subscription = Subscription.objects.filter(
            user=user,
            course=course
        )

        if subscription.exists():

            subscription.delete()

            message = "Подписка удалена"

        else:

            Subscription.objects.create(
                user=user,
                course=course
            )

            message = "Подписка добавлена"

        return Response(
            {
                "message": message
            }
        )
