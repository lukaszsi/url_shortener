from django.core.validators import MinLengthValidator, RegexValidator
import uuid
from django.db import models


class ShortenedURL(models.Model):
    SHORT_CODE_LENGTH = 6

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # **Aditional context**
    # I decided to NOT to make original_url field unique and to not to respond with the same
    # short url/code for the same original url. This decision though might be different, based
    # on the business requirements - this affects, among other things, possibility to track
    # usages of the short urls by individual users, ability to independently disable individual
    # short urls, etc. In real-work case, I'd discuss with the stakeholders and the team before
    # making this decision.
    original_url = models.URLField()
    short_code = models.CharField(
        max_length=SHORT_CODE_LENGTH,
        unique=True,
        db_index=True,
        validators=[
            MinLengthValidator(SHORT_CODE_LENGTH),  # Ensures exact characters length
            RegexValidator(
                regex=r"^[a-zA-Z0-9]+$",  # Allows only alphanumeric characters to not to break any url
                message="Short code must contain only letters and numbers.",
                code="invalid_short_code",
            ),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"
