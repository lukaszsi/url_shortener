from django.test import TestCase
from shortener.models import ShortenedURL
from django.core.exceptions import ValidationError
import uuid


class ShortenedURLModelTest(TestCase):
    def setUp(self):
        """Set up test data for each test"""
        self.valid_url = "https://example.com/some/long/url"
        self.short_code = "abc123"

    def test_create_shortened_url(self):
        """Test that a ShortenedURL object can be created correctly"""
        short_url = ShortenedURL.objects.create(
            original_url=self.valid_url, short_code=self.short_code
        )
        self.assertEqual(short_url.original_url, self.valid_url)
        self.assertEqual(short_url.short_code, self.short_code)
        self.assertIsInstance(short_url.id, uuid.UUID)

    def test_short_code_must_be_unique(self):
        """Test that the short_code field must be unique"""
        ShortenedURL.objects.create(original_url=self.valid_url, short_code="abc123")

        with self.assertRaises(
            Exception
        ):  # Django raises IntegrityError for unique constraint violations
            ShortenedURL.objects.create(
                original_url="https://example.com/another/url", short_code="abc123"
            )

    def test_short_code_validation(self):
        """Test that short_code must be alphanumeric characters only and of proper length"""
        short_url = ShortenedURL(
            original_url=self.valid_url, short_code="12345"
        )  # Too short
        with self.assertRaises(ValidationError):
            short_url.full_clean()  # Triggers model field validators

        short_url.short_code = "abcdefg"  # Too long
        with self.assertRaises(ValidationError):
            short_url.full_clean()

        short_url.short_code = "abc/12"  # Invalid character, this could break url
        with self.assertRaises(ValidationError):
            short_url.full_clean()

    def test_original_url_can_repeat(self):
        """Test that original_url does NOT need to be unique"""
        ShortenedURL.objects.create(original_url=self.valid_url, short_code="code01")
        ShortenedURL.objects.create(original_url=self.valid_url, short_code="code02")

        count = ShortenedURL.objects.filter(original_url=self.valid_url).count()
        self.assertEqual(count, 2)

    def test_default_uuid_generation(self):
        """Test that UUID is automatically generated"""
        short_url = ShortenedURL.objects.create(
            original_url=self.valid_url, short_code="xyz789"
        )
        self.assertIsNotNone(short_url.id)
        self.assertIsInstance(short_url.id, uuid.UUID)
