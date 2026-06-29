from rest_framework.viewsets import ModelViewSet
from .models import Course
from .serializers import CourseSerializer
from .models import Lesson
from .serializers import LessonSerializer

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)



class LessonListCreateAPIView(ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
