from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CourseViewSet,
    LessonViewSet,
    PaymentCreateAPIView,
    PaymentViewSet,
    SubscriptionAPIView,
)

router = DefaultRouter()


router.register(r"courses", CourseViewSet, basename="courses")


router.register(r"lessons", LessonViewSet, basename="lessons")


router.register(r"payments", PaymentViewSet, basename="payments")


urlpatterns = [
    path(
        "payments/create/",
        PaymentCreateAPIView.as_view(),
        name="payment-create",
    ),
    path("", include(router.urls)),
    path(
        "subscription/",
        SubscriptionAPIView.as_view(),
        name="subscription",
    ),
]
