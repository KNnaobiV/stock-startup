from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
__all__ = [
    "validate_account_number", 
    "validate_bvn",
    "validate_phone_number",
]

def validate_account_number(value):
    if len(str(value)) > 10 or len(str(value)) < 10:
        raise ValidationError(
            _(f'{value} is not ten digits, phone must be 10 digits.')
        )


def validate_bvn(value):
    if len(str(value)) != 10:
        raise ValidationError(
            _f(f'{value} is not ten digits, bvn must be 10 digits.')
        )

def validate_phone_number(value):
    if len(value) > 11 or len(value) < 11:
        raise ValidationError(
            _(f'{value} is not eleven digits, phone must be 11 digits ')
        )