from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.core.exceptions import ValidationError
from django.db.models import F, QuerySet

from core.services import recipe_amount_ingredients_set, Base64ImageField
from core.validators import ingredients_validator, tags_validator
from users.models import CustomUser
from recipes.models import Ingredient, Recipe, Tag


class CropRecipeSerializer(ModelSerializer):
    """Сериализатор вывода рецептов по подпискам."""
    class Meta:
        model = Recipe
        fields = "id", "name", "image", "cooking_time"
        read_only_fields = ("__all__",)


class UserSerializer(ModelSerializer):
    """Сериализатор для использования с моделью CustomUser."""
    is_subscribed = SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ("is_subscribed",)

    def get_is_subscribed(self, obj: CustomUser) -> bool:
        """Проверка подписки.
        Метод проверяет авторизацию и подписку.
        Если запись найдена, возвращает True.
        """
        user = self.context.get("view").request.user
        if user.is_anonymous or (user == obj):
            return False
        return user.subscriptions.filter(author=obj).exists()

    def create(self, validated_data: dict) -> CustomUser:
        """Создание нового пользователя."""
        user = CustomUser(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserSubscribeSerializer(UserSerializer):
    """Сериализатор вывода подписок пользователя."""
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )
        read_only_fields = ("__all__",)

    def get_recipes(self, obj):
        recipes = obj.recipes.all()[:3]
        serializer = CropRecipeSerializer(recipes, many=True, read_only=True)
        return serializer.data

    def get_is_subscribed(*args) -> bool:
        """Сериализатор выводит только подписчиков.
        Метод возвращает True.
        """
        return True

    def get_recipes_count(self, obj: CustomUser) -> int:
        """Количество рецептов у автора."""
        return obj.recipes.count()


class TagSerializer(ModelSerializer):
    """Сериализатор для вывода тэгов."""

    class Meta:
        model = Tag
        fields = ("__all__")
        read_only_fields = ("__all__",)


class IngredientSerializer(ModelSerializer):
    """Сериализатор для модели Ingredient."""

    class Meta:
        model = Ingredient
        fields = ("__all__")
        read_only_fields = ("__all__",)


class RecipeSerializer(ModelSerializer):
    """Сериализатор для рецептов."""
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        read_only_fields = (
            "is_favorite",
            "is_in_shopping_cart",
        )

    def get_ingredients(self, recipe: Recipe) -> QuerySet:
        """Список ингридиентов для рецепта."""
        ingredients = recipe.ingredients.values(
            "id", "name", "measurement_unit", amount=F("recipe__amount")
        )
        return ingredients

    def get_is_favorited(self, recipe: Recipe) -> bool:
        """Проверка добавления в избранное.
        Метод проверяет авторизацию и наличие объекта.
        Если запись найдена, возвращает True.
        """
        user = self.context.get("view").request.user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe: Recipe) -> bool:
        """Проверка добавления в корзину.
        Метод проверяет авторизацию и наличие объекта.
        Если запись найдена, возвращает True.
        """
        if not isinstance(recipe, Recipe):
            return False
        user = self.context.get("view").request.user
        if user.is_anonymous:
            return False
        return user.carts.filter(recipe=recipe).exists()

    def validate(self, data: dict) -> dict:
        """Проверка данных при создании рецепта."""
        tags_obj: list = self.initial_data.get("tags")
        ingredients: list = self.initial_data.get("ingredients")

        if not tags_obj or not ingredients:
            raise ValidationError("Не введены данные")

        tags_validator(tags_obj, Tag)
        ingredients = ingredients_validator(ingredients, Ingredient)
        data.update({
            "tags": tags_obj,
            "ingredients": ingredients,
            "author": self.context.get("request").user
        })
        return data

    def create(self, validated_data: dict) -> Recipe:
        """Создание нового рецепта."""
        tags: list = validated_data.pop("tags")
        ingredients: list = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)
        recipe_amount_ingredients_set(recipe, ingredients)
        recipe.tags.set(tags)
        return recipe

    def update(self, recipe: Recipe, validated_data: dict):
        """Обновление рецепта."""
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")

        for key, value in validated_data.items():
            if hasattr(recipe, key):
                setattr(recipe, key, value)
        if tags:
            recipe.tags.clear()
            recipe.tags.set(tags)
        if ingredients:
            recipe.ingredients.clear()
            recipe_amount_ingredients_set(recipe, ingredients)
        recipe.save()
        return recipe
