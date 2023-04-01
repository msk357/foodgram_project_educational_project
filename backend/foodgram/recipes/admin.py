from django.contrib.admin import ModelAdmin
from django.utils.safestring import SafeString, mark_safe
from django.contrib import admin

from .forms import TagForm
from .models import AmountIngredient, Cart, Favorit, Ingredient, Recipe, Tag
from core.enums import Tuples


class TagAdmin(ModelAdmin):
    form = TagForm
    list_display = (
        "name",
        "slug",
        "color",
    )
    search_fields = (
        "name",
        "color",
    )

    save_on_top = True
    empty_value_display = Tuples.EMPTY_VALUE_DISPLAY.value


class IngredientAdmin(ModelAdmin):
    list_display = (
        "name",
        "measurement_unit",
    )
    search_fields = ("name",)
    list_filter = ("name",)

    save_on_top = True
    empty_value_display = Tuples.EMPTY_VALUE_DISPLAY.value


class RecipeAdmin(ModelAdmin):
    list_display = (
        "name",
        "author",
        "get_image",
        "count_favorites",
        "image",
    )
    fields = (
        (
            "name",
            "cooking_time",
        ),
        (
            "author",
            "tags",
        ),
        ("text",),
        ("image",),
    )
    raw_id_fields = ("author",)
    filter_horizontal = ["tags"]
    search_fields = (
        "name",
        "author__username",
        "tags__name",
    )
    list_filter = (
        "name",
        "author__username",
        "tags__name",
    )

    save_on_top = True
    empty_value_display = Tuples.EMPTY_VALUE_DISPLAY.value

    def get_image(self, obj: Recipe) -> SafeString:
        if obj.image:
            return mark_safe(
                f'<img src={obj.image.url} width="50" hieght="20"'
            )

    def count_favorites(self, obj: Recipe) -> int:
        return obj.in_favorites.count()


class FavoriteAdmin(ModelAdmin):
    list_display = (
        "user",
        "recipe",
        "date_added",
    )
    search_fields = (
        "user__username",
        "recipe__name",
    )
    empty_value_display = Tuples.EMPTY_VALUE_DISPLAY.value


class CartAdmin(ModelAdmin):
    list_display = (
        "user",
        "recipe",
        "date_added",
    )
    search_fields = (
        "user__username",
        "recipe__name",
    )
    empty_value_display = Tuples.EMPTY_VALUE_DISPLAY.value


class AmountIngredientAdmin(ModelAdmin):
    list_display = (
        "recipe",
        "ingredients",
        "amount",
    )
    search_fields = (
        "recipe",
        "amount",
        "ingredients",
    )
    empty_value_display = Tuples.EMPTY_VALUE_DISPLAY.value


admin.site.register(AmountIngredient, AmountIngredientAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favorit, FavoriteAdmin)
admin.site.register(Cart, CartAdmin)

admin.site.site_title = "Админ-панель сайта Foodgram"
admin.site.site_header = "Админ-панель сайта Foodgram"
