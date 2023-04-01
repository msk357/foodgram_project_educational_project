"""Модели для управления пользователями.
Models:
    CustomUser:
        Создана кастомная модель для юзеров.
        Добавлено поле is_active для работы со статусом.
    Follow:
       Стандартная модель для подписчиков.
       Добавлено условие UniqueConstraint.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import validate_email
from django.db.models import F, Q

from core.enums import Limits
from core.validators import validate_field_name

class CustomUser(AbstractUser):
    """Модель для пользователей.
    В модели добавлен метод clean для валидации полей.
    Поля модели:
        first_name:
            Имя пользователя, добавлена валидация.
        last_name:
            Фамилия пользователя, добавлена валидация.
        username:
            Логин пользователя, добавлена валидация.
        email:
            Почта пользователя.
            Добавлена стандартная валидация.
        is_active:
            Статус пользователя (bool).
    """
    first_name = models.CharField(
        verbose_name="Имя пользователя",
        max_length=Limits.MAX_LEN_NAME.value,
        help_text="Введите ваше имя",
    )
    last_name = models.CharField(
        verbose_name="Фамилия пользователя",
        max_length=Limits.MAX_LEN_NAME.value,
        help_text="Введите вашу фамилию",
    )
    username = models.CharField(
        verbose_name="Логин пользователя",
        max_length=Limits.MAX_LEN_NAME.value,
        unique=True,
        help_text="Введите ваш логин",
    )
    email = models.EmailField(
        max_length=Limits.MAX_LEN_EMAIL_FIELD.value,
        help_text="Введите ваш email",
        unique=True,
        validators=[validate_email],
    )
    password = models.CharField(
        verbose_name="Пароль", max_length=128, help_text="Укажите пароль"
    )
    is_active = models.BooleanField(
        verbose_name="Статус активирован",
        default=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_username(self):
        return self.email

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def clean(self) -> None:
        self.username = validate_field_name(self.username)
        return super().clean()

    def __str__(self) -> str:
        return f"Пользователь: {self.username}"


class Follow(models.Model):
    """Модель для подписчиков.
    Поля модели:
        user:
            Подписчик.
        author:
            Автор рецепта.
    """
    user = models.ForeignKey(
        CustomUser,
        verbose_name="Подписчик",
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    author = models.ForeignKey(
        CustomUser,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="subscribers",
    )
    date_added = models.DateTimeField(
        verbose_name='Дата создания подписки',
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'user'),
                name='\nRepeat subscription\n',
            ),
            models.CheckConstraint(
                check=~Q(author=F('user')),
                name='\nNo self subscription\n'
            )
        )

    def __str__(self):
        return f"{self.user} подписан на {self.author}"
