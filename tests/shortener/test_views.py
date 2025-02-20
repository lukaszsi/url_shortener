from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from shortener.models import ShortenedURL


class ShortenURLViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_url = "https://example.com/some/long/url"
        self.invalid_url = "not_a_valid_url"
        self.endpoint = reverse("shorten-url")

    def test_shorten_valid_url(self):
        """Test shortening a valid URL returns a 201 response with a shortened URL"""
        response = self.client.post(
            self.endpoint, {"url": self.valid_url}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("short_url", response.data)

        short_url = response.data["short_url"]
        self.assertTrue(short_url.startswith(f"{settings.BASE_URL}/shrt/"))

        short_code = short_url.split("/")[-1]
        self.assertTrue(ShortenedURL.objects.filter(short_code=short_code).exists())

    def test_shorten_invalid_url(self):
        """Test sending an invalid URL returns a 400 response"""
        response = self.client.post(
            self.endpoint, {"url": self.invalid_url}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("url", response.data)

    def test_shorten_missing_url(self):
        """Test sending an empty request body returns a 400 response"""
        response = self.client.post(self.endpoint, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("url", response.data)

    def test_shorten_duplicate_url_generates_different_codes(self):
        """Test that shortening the same URL multiple times generates unique short codes"""
        response_1 = self.client.post(
            self.endpoint, {"url": self.valid_url}, format="json"
        )
        response_2 = self.client.post(
            self.endpoint, {"url": self.valid_url}, format="json"
        )

        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_2.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response_1.data["short_url"], response_2.data["short_url"])

    def test_shorten_url_stored_correctly(self):
        """Test that a shortened URL is stored correctly in the database"""
        response = self.client.post(
            self.endpoint, {"url": self.valid_url}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        short_code = response.data["short_url"].split("/")[-1]
        url_entry = ShortenedURL.objects.get(short_code=short_code)
        self.assertEqual(url_entry.original_url, self.valid_url)


class ExpandURLViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.original_url = "https://example.com/some/long/url"

        self.shortened_instance = ShortenedURL.objects.create(
            original_url=self.original_url,
            short_code="abc123",
        )

        self.expand_endpoint = reverse(
            "expand-url", kwargs={"short_code": self.shortened_instance.short_code}
        )
        self.non_existent_expand_endpoint = reverse(
            "expand-url", kwargs={"short_code": "xxxxxx"}
        )

    def test_expand_valid_short_code(self):
        """Test expanding a valid short code returns the correct original URL"""
        response = self.client.get(self.expand_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("original_url", response.data)
        self.assertEqual(response.data["original_url"], self.original_url)

    def test_expand_non_existent_short_code(self):
        """Test expanding a non-existent short code returns a 404 error"""
        response = self.client.get(self.non_existent_expand_endpoint)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Short code not found.")

    def test_expand_invalid_short_code(self):
        """Test that an invalid short code format (too short) returns a 400 error"""
        invalid_expand_endpoint = reverse(
            "expand-url", kwargs={"short_code": "abc"}
        )
        response = self.client.get(invalid_expand_endpoint)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "short_code", response.data
        )


class RedirectShortURLViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.original_url = "https://example.com/some/long/url"

        self.shortened_instance = ShortenedURL.objects.create(
            original_url=self.original_url,
            short_code="abc123",
        )

        self.redirect_endpoint = reverse(
            "redirect-url", kwargs={"short_code": self.shortened_instance.short_code}
        )

        self.non_existent_redirect_endpoint = reverse(
            "redirect-url", kwargs={"short_code": "xxxxxx"}
        )

    def test_redirect_valid_short_code(self):
        """Test that accessing a valid short code redirects to the original URL"""
        response = self.client.get(self.redirect_endpoint)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response["Location"], self.original_url)

    def test_redirect_non_existent_short_code(self):
        """Test that accessing a non-existent short code returns a 404 error"""
        response = self.client.get(self.non_existent_redirect_endpoint)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
