"""Модели для управления рецептами.
Models:
    Recipe:
        Основная модель для рецептов.
    Tag:
       Модель для описания тэгов.
       Связана с Recipe через Many-To-Many.
    Ingredient:
        Модель для описания ингредиентов.
        Связана с Recipe через модель AmountIngredient.
    AmountIngredient:
        Модель для Ingredient и Recipe.
        Считает кол-во ингридиента.
    Favorite:
        Избранные пользователем рецепты.
    Cart:
        Рецепты в корзине покупок.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import CustomUser
from core.enums import Limits
from core.validators import (hex_validator_code,
                             validate_field_name,
                             validate_field_slug)


class Tag(models.Model):
    """Модель для тэгов.
    Связана с моделью Recipe через М2М.
    В модели добавлен метод clean для валидации полей.
    Поля модели:
        name:
            Название тэга. Поле не должно совпалать с slug.
            В поле разрешены только буквы.
        color:
            Цвет тэга в HEX-кодировке. Добавлен валидатор.
        slug:
            В поле разрешены только буквы.
    """
    name = models.CharField(
        verbose_name="Название тeга",
        max_length=Limits.MAX_LEN_NAME.value,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name="Slug тега",
        max_length=Limits.MAX_LEN_SLUG.value,
        unique=True,
    )
    color = models.CharField(
        verbose_name="Цвет тега",
        max_length=7,
        unique=True
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                fields=["name", "slug"],
                name="unique_tag"
            ),
        ]

    def clean(self) -> None:
        self.name = validate_field_name(self.name)
        self.color = hex_validator_code(self.color)
        self.slug = validate_field_slug(self.slug)
        return super().clean()

    def __str__(self):
        return f"{self.name} цвет тега: {self.color}"


class Ingredient(models.Model):
    """Модель для ингридиентов.
    Связана с моделью Recipe через М2М.
    В модели добавлен метод clean для валидации полей.
    Поля модели:
        name:
            Название ингридиента. Разрешены только буквы.
        measurement_unit:
            Единица измерения ингридиента.
    """
    name = models.CharField(
        max_length=Limits.MAX_LEN_NAME.value,
        verbose_name="Название ингридиента",
        help_text="Введите название ингридиента",
    )
    measurement_unit = models.CharField(
        verbose_name="Единица измерения",
        max_length=Limits.MAX_LEN_MEASUREMENT.value
    )

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                fields=["name", "measurement_unit"], name="unique_ingredients"
            )
        ]

    def clean(self) -> None:
        self.name = validate_field_name(self.name)
        self.measurement_unit = self.measurement_unit.lower()
        return super().clean()

    def __str__(self) -> str:
        return f"Ингридиент: {self.name}"


class Recipe(models.Model):
    """Основная модель с рецептами.
    Связана с моделью Recipe через М2М.
    В модели добавлен метод clean для валидации полей.
    Поля модели:
       name:
            Название рецепта.
        author:
            Автор рецепта, связан с моделю CustomerUser.
        in_favorites:
            Связь M2M с моделью CustomerUser.
        tags:
            Связь M2M с моделью Tag.
        ingredients:
            Связь M2M с моделью Ingredient. Добавлена модель
            AmountIngredient с указанием количества ингридиентов.
        in_carts(int):
            Связь M2M с моделью CustomerUser.
            Используется при добавлении рецепта в `покупки`.
        pub_date(datetime):
            Дата добавления рецепта.
        image:
            Изображение рецепта.
        text:
            Описание рецепта.
        cooking_time:
            Время приготовления рецепта. Добавлена валидация.
    """
    author = models.ForeignKey(
        CustomUser,
        verbose_name="Автор рецепта",
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    name = models.CharField(
        verbose_name="Название рецепта",
        max_length=Limits.MAX_LEN_NAME.value,
        help_text="Напишите название рецепта",
    )
    text = models.TextField(
        verbose_name="Описание рецепта",
        max_length=Limits.MAX_LEN_TEXT.value,
        help_text="Напишите описание рецепта",
    )
    image = models.ImageField(
        verbose_name="Картинка",
        upload_to="recipes/images/",
        help_text="Добавьте изображение",
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления",
        help_text="Укажите время в минутах",
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(500)],
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name="Ингредиенты",
        related_name="recipes",
        through="recipes.AmountIngredient",
    )
    pub_date = models.DateField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Тег",
        related_name="recipes",
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ('-pub_date',)

    def clean(self) -> None:
        self.name = validate_field_name(self.name)
        return super().clean()

    def __str__(self) -> str:
        return f"Рецепт: {self.name}"


class AmountIngredient(models.Model):
    """Модель для определения веса ингридиента в рецепте.
    Связывает Recipe и Ingredient.
    Поля модели:
        recipe:
            Рецепт через ForeignKey.
        ingredients:
            Ингридиент через ForeignKey.
        amount:
            Количество ингридиентов в рецепте.
    """
    recipe = models.ForeignKey(
        Recipe,
        verbose_name="В каком рецепте",
        related_name="ingredient",
        on_delete=models.CASCADE,
    )
    ingredients = models.ForeignKey(
        Ingredient,
        verbose_name="Ингредиенты в рецептах",
        related_name="recipe",
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество",
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
    )

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Количество ингридиентов"
        ordering = ('recipe', )
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredients"], name="unique_ingredient"
            )
        ]

    def __str__(self) -> str:
        return f"{self.ingredients}"


class Favorit(models.Model):
    """Модель для добавления в избранное.
    Связывает Recipe и CustomerUser.
    Поля модели:
        recipe:
            Рецепт через ForeignKey.
        user:
            Пользователь через ForeignKey.
        date_added:
            Дата добавления рецепта.
    """
    recipe = models.ForeignKey(
        Recipe,
        verbose_name="Избранные рецепты",
        related_name="in_favorites",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        CustomUser,
        verbose_name="Пользователь",
        related_name="favorites",
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        verbose_name="Дата добавления", auto_now_add=True, editable=False
    )

    class Meta:
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"
        constraints = (
            models.UniqueConstraint(
                fields=["recipe", "user"],
                name="unique_favorites"
            ),
        )

    def __str__(self) -> str:
        return f"{self.user} добавил в избранное {self.recipe}"


class Cart(models.Model):
    """Модель для добавления в корзину.
    Связывает Recipe и CustomerUser.
    Поля модели:
        recipe:
            Рецепт через ForeignKey.
        user:
            Пользователь через ForeignKey.
        date_added:
            Дата добавления рецепта.
    """
    recipe = models.ForeignKey(
        Recipe,
        verbose_name="Рецепты в корзине",
        related_name="in_shopping_cart",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        CustomUser,
        verbose_name="Владелец списка",
        related_name="carts",
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        verbose_name="Дата добавления", auto_now_add=True
    )

    class Meta:
        verbose_name = "Рецепт в списке покупок"
        verbose_name_plural = "Рецепты в списке покупок"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "user"],
                name="unique_cart"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user} добавил в корзину {self.recipe}"
