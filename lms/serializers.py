from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from .models import Course, Lesson, Payment
from .validators import YouTubeValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [
            YouTubeValidator(field="video_url")
        ]


class CourseSerializer(serializers.ModelSerializer):

    lessons = LessonSerializer(
        many=True,
        read_only=True
    )

    lessons_count = serializers.SerializerMethodField()

    is_subscribed = serializers.SerializerMethodField()


    class Meta:
        model = Course
        fields = "__all__"


    @extend_schema_field(int)
    def get_lessons_count(self, obj):
        return obj.lessons.count()


    @extend_schema_field(bool)
    def get_is_subscribed(self, obj):

        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return False

        return obj.subscriptions.filter(
            user=request.user
        ).exists()



class PaymentSerializer(serializers.ModelSerializer):

    class Meta:

        model = Payment

        fields = "__all__"

        read_only_fields = [
            "user",
            "payment_date",

            "stripe_product_id",
            "stripe_price_id",
            "stripe_session_id",

            "payment_link",

            "status",
        ]
