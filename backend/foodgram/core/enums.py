"""Настройки переменных."""
from enum import Enum, IntEnum


class Tuples(tuple, Enum):
    # размер изображения
    RECIPE_IMAGE = 500, 300
    # значение для empty_value_display
    EMPTY_VALUE_DISPLAY = "Нет значения"
    # поиск по параметрам
    SYMBOL_TRUE_SEARCH = "1", "true"
    SYMBOL_FALSE_SEARCH = "0", "false"
    # типы запросов
    ADD_METHODS = "GET", "POST"
    DEL_METHODS = ("DELETE",)
    ACTION_METHODS = "GET", "POST", "DELETE"
    UPDATE_METHODS = "PUT", "PATCH"


class Limits(IntEnum):
    # Максимальная длина email для моделей
    MAX_LEN_EMAIL_FIELD = 256
    # Максимальная длина для поля name в моделях
    MAX_LEN_NAME = 70
    # Максимальная длина для поля slug в моделях
    MAX_LEN_SLUG = 64
    # Максимальная длина единицы измерения для модели "Ingredient"
    MAX_LEN_MEASUREMENT = 256
    # Максимальная длина текстовых полей в моделях
    MAX_LEN_TEXT = 5000


class UrlRequests(str, Enum):
    # Параметр для поиска ингридиентов
    SEARCH_ING_NAME = "name"
    # Параметр для поиска в списке "избранное"
    FAVORIT = "is_favorited"
    # Параметр для поиска в списке "покупки"
    SHOP_CART = "is_in_shopping_cart"
    # Параметр для поиска по автору
    AUTHOR = "author"
    # Параметр для поиска объектов по тэгам
    TAGS = "tags"
