from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModerator, IsOwner


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="moderators").exists():
            return Course.objects.all()

        return Course.objects.filter(owner=user)

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
        serializer.save(owner=self.request.user)



class LessonViewSet(ModelViewSet):
    serializer_class = LessonSerializer


    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=user)



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
        serializer.save(owner=self.request.user)
