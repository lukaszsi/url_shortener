from rest_framework import serializers
from shortener.models import ShortenedURL


class ShortenedURLSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)


class ExpandURLSerializer(serializers.Serializer):
    short_code = serializers.CharField(
        max_length=ShortenedURL.SHORT_CODE_LENGTH,
        # Using model's validators to ensure consistency
        validators=ShortenedURL._meta.get_field("short_code").validators,
    )
