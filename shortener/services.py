# **Aditional context**
# I'm aware that creating separate service layer might be an overkill for such a simple app.
# We could also i.e. go with 'fat models approach' and encapsulate all the logic in the models.
import random
import string
from shortener.models import ShortenedURL


def generate_unique_short_code(length=ShortenedURL.SHORT_CODE_LENGTH, max_attempts=3):
    """Generate a unique short code, retrying up to `max_attempts` times if necessary."""
    for _ in range(max_attempts):
        short_code = "".join(
            random.choices(string.ascii_letters + string.digits, k=length)
        )
        if not ShortenedURL.objects.filter(short_code=short_code).exists():
            return short_code
    raise ValueError("Failed to generate a unique short code after multiple attempts.")


def create_shortened_url(original_url):
    """Creates a shortened URL instance with a unique short code."""
    try:
        short_code = generate_unique_short_code()
        short_url_instance = ShortenedURL.objects.create(
            original_url=original_url, short_code=short_code
        )
        return short_url_instance
    except Exception as e:
        raise ValueError(f"Error creating shortened URL: {str(e)}")
