from django.test import TestCase
from shortener.serializers import ExpandURLSerializer, ShortenedURLSerializer


class ShortenedURLSerializerTest(TestCase):
    def setUp(self):
        self.valid_url = "https://example.com/some/long/url"
        self.invalid_url = "not_a_valid_url"

    def test_valid_serializer(self):
        """Test that serializer validates a correct URL"""
        data = {"url": self.valid_url}
        serializer = ShortenedURLSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_url(self):
        """Test that serializer rejects an invalid URL"""
        data = {"url": self.invalid_url}
        serializer = ShortenedURLSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("url", serializer.errors)


class ExpandURLSerializerTest(TestCase):
    def setUp(self):
        self.valid_short_code = "abc123"  # Valid alphanumeric short code
        self.invalid_short_code_too_short = "abc"  # Too short
        self.invalid_short_code_too_long = "abcdefgh"  # Too long
        self.invalid_short_code_special_chars = "abc/12"  # Contains special characters

    def test_valid_short_code(self):
        """Test that serializer accepts a valid short code"""
        data = {"short_code": self.valid_short_code}
        serializer = ExpandURLSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_short_code_too_short(self):
        """Test that serializer rejects short codes that are too short"""
        data = {"short_code": self.invalid_short_code_too_short}
        serializer = ExpandURLSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("short_code", serializer.errors)

    def test_short_code_too_long(self):
        """Test that serializer rejects short codes that are too long"""
        data = {"short_code": self.invalid_short_code_too_long}
        serializer = ExpandURLSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("short_code", serializer.errors)

    def test_short_code_with_special_chars(self):
        """Test that serializer rejects short codes containing special characters"""
        data = {"short_code": self.invalid_short_code_special_chars}
        serializer = ExpandURLSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("short_code", serializer.errors)
