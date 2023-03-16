"""Модуль для валидации данных.
   Методы модуля:
        hex_validator_code:
            Используется стандартная валидация RegexValidator.
            Проверяется наличие знака # и цифр.
        validate_field_name:
            Проверка имени на длину и символы.
        validate_field_slug:
            Проверка поля slug.
            Длина от 2-х до 50-ти символов.
            Используются только цифры и буквы.
"""
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.text import slugify


def hex_validator_code(color: str) -> str:
    hex_validator = RegexValidator(
        regex="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
        message="Введите hex-код",
        code="Неправильный код",
    )
    if hex_validator(color) is None:
        return color
    raise ValidationError("Неправильный код")


def validate_field_name(name: str) -> str:
    if len(name) < 2:
        raise ValidationError(
            "Имя должно быть длинее 2-х символов"
        )
    if not name.isalpha():
        raise ValidationError(
            "Имя должно содержать только буквы"
        )
    if name == "me":
        raise ValidationError(
            "Использовать 'me' в качестве username запрещено"
        )
    return name.capitalize().strip()


def validate_field_slug(slug: str) -> str:
    slug_valid = slugify(slug)
    if len(slug_valid) < 2:
        raise ValidationError("Slug не должен быть менее 2 символов")
    if len(slug_valid) > 50:
        raise ValidationError("Slug не должен превышать длину 50 символов")
    if not slug_valid.isalnum():
        raise ValidationError("Slug должен содеражать только цифры и буквы")
    return slug_valid.capitalize().strip()
