from django.test import TestCase
from shortener.services import create_shortened_url
from unittest.mock import patch
from shortener.models import ShortenedURL


class ShortenedURLServiceTest(TestCase):
    def setUp(self):
        self.valid_url = "https://example.com/some/long/url"

    def test_create_shortened_url(self):
        """Test that a shortened URL is successfully created"""
        short_url_instance = create_shortened_url(self.valid_url)
        self.assertEqual(short_url_instance.original_url, self.valid_url)
        self.assertEqual(
            len(short_url_instance.short_code), ShortenedURL.SHORT_CODE_LENGTH
        )
        self.assertTrue(short_url_instance.short_code.isalnum())

    def test_create_shortened_url_error_handling(self):
        """Test that an error is raised when short_code generation fails"""
        with patch(
            "shortener.services.generate_unique_short_code",
            side_effect=ValueError("Failed to generate"),
        ):
            with self.assertRaises(ValueError) as error:
                create_shortened_url(self.valid_url)

            self.assertIn("Failed to generate", str(error.exception))
