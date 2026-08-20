from rest_framework.serializers import ValidationError


class YouTubeValidator:
    """
    Разрешает только ссылки на youtube.com.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        url = attrs.get(self.field)

        if not url:
            return

        if "youtube.com" not in url:
            raise ValidationError("Разрешены ссылки только на youtube.com.")
