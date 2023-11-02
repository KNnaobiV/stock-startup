from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
__all__ = [
    "validate_phone_number",
]


def validate_phone_number(value):
    if len(value) > 11 or len(value) < 11:
        raise ValidationError(
            _(f'{value} is not eleven digits, phone must be 11 digits ')
        )