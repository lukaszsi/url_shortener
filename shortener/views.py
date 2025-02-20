from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from shortener.models import ShortenedURL
from shortener.serializers import ExpandURLSerializer, ShortenedURLSerializer
from shortener.services import create_shortened_url


class ShortenURLView(APIView):
    """API endpoint to create a shortened URL"""

    def post(self, request, *args, **kwargs) -> Response:
        serializer = ShortenedURLSerializer(data=request.data)
        if serializer.is_valid():
            try:
                short_url_instance = create_shortened_url(
                    serializer.validated_data["url"]
                )
                short_url = f"{settings.BASE_URL}/shrt/{short_url_instance.short_code}"
                return Response(
                    {"short_url": short_url}, status=status.HTTP_201_CREATED
                )
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpandURLView(APIView):
    """API endpoint to expand a shortened URL."""

    def get(self, request, short_code: str, *args, **kwargs) -> Response:
        serializer = ExpandURLSerializer(data={"short_code": short_code})
        if serializer.is_valid():
            validated_code = serializer.validated_data["short_code"]
            try:
                instance = ShortenedURL.objects.get(short_code=validated_code)
            except ShortenedURL.DoesNotExist:
                return Response(
                    {"error": "Short code not found."}, status=status.HTTP_404_NOT_FOUND
                )
            return Response(
                {"original_url": instance.original_url}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RedirectShortURLView(APIView):
    """API endpoint to redirect from a shortened URL to the original URL."""

    def get(self, request, short_code: str, *args, **kwargs) -> HttpResponseRedirect:
        short_url_instance = get_object_or_404(ShortenedURL, short_code=short_code)
        return HttpResponseRedirect(short_url_instance.original_url)
