from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


USER_EMAIL_MAX_LENGTH = 254
USER_USERNAME_MAX_LENGTH = 150


class FoodgramUser(AbstractUser):
    """
    Модель пользователей.
    """

    USER = 'user'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'пользователь'),
        (ADMIN, 'администратор')
    ]

    email = models.EmailField(
        max_length=USER_EMAIL_MAX_LENGTH,
        unique=True,
        verbose_name='Электронная почта'
    )
    status = models.CharField(
        choices=ROLE_CHOICES,
        default=USER,
        max_length=20,
        verbose_name='Статус пользователя на сайте'
    )
    username = models.CharField(
        max_length=USER_USERNAME_MAX_LENGTH,
        unique=True,
        validators=(UnicodeUsernameValidator(),),
        verbose_name='Никнейм'
    )
    first_name = models.CharField(
        max_length=30,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    password = models.CharField(
        max_length=128,
        verbose_name='Пароль'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', 'password')

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_user_role(self):
        return self.status == self.USER

    @property
    def is_admin_role(self):
        return self.status == self.ADMIN

    @property
    def get_recipes_count(self):
        return self.recipe.count()
