from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Follow
from core.enums import Tuples


class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "last_name",
        "email",
        "first_name",
    )
    list_filter = (
        "email",
        "first_name",
    )
    search_fields = (
        "email",
        "username",
    )
    ordering = (
        "email",
        "username",
    )

    empty_value_display = Tuples.EMPTY_VALUE_DISPLAY.value


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "author",
    )
    search_fields = (
        "user",
        "author",
    )
    list_filter = (
        "user",
        "author",
    )

    empty_value_display = Tuples.EMPTY_VALUE_DISPLAY.value


admin.site.register(Follow, FollowAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
