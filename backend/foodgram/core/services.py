"""Модуль для дополнительных методов сериализаторов.
   Методы модуля:
        recipe_amount_ingredients_set:
            Создаёт объект AmountIngredient, связывающий Recipe и
            Ingredient.
        Base64ImageField:
            Работа с изображением. Дешифровка изображдения.
"""
from recipes.models import Recipe, AmountIngredient

import base64
from django.core.files.base import ContentFile
from rest_framework import serializers


def recipe_amount_ingredients_set(recipe: Recipe, ingredients: list[dict]):
    for ingredient in ingredients:
        AmountIngredient.objects.get_or_create(
            recipe=recipe,
            ingredients=ingredient["ingredient"],
            amount=ingredient["amount"],
        )


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)
        return super().to_internal_value(data)
