from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import (
    RegexValidator, MinValueValidator, MaxValueValidator)

from users.models import FoodgramUser

MAX_LENGHTH = 20


def format_string(field1, field2):
    len_field1 = len(field1)
    len_field2 = len(field2)

    if len_field1 > MAX_LENGHTH and len_field2 > MAX_LENGHTH:
        return f'{field1[:MAX_LENGHTH]}... - {field2[:MAX_LENGHTH]}...'
    elif len_field1 > MAX_LENGHTH and len_field2 <= MAX_LENGHTH:
        return f'{field1[:MAX_LENGHTH]}... - {field2}'
    elif len_field1 <= MAX_LENGHTH and len_field2 > MAX_LENGHTH:
        return f'{field1} - {field2[:MAX_LENGHTH]}...'
    else:
        return f'{field1} - {field2}'


def leight_field(field):
    if len(field) > MAX_LENGHTH:
        return field[:MAX_LENGHTH] + '...'
    else:
        return field


def lowercase_validator(value):
    if value != value.lower():
        raise ValidationError("Цвет тега должен быть в нижнем регистре.")


class Tag(models.Model):
    """Модель для хранения тегов."""

    name = models.CharField('Название тега', max_length=200)
    color = models.CharField(
        'Цвет тега',
        unique=True,
        max_length=7,
        validators=[
            RegexValidator(
                regex=r'^#[a-z0-9]{0,6}$',
                message='Неверное значение. Допускаются только цифры, '
                'символ #(обратите внимание,что символ # должен быть первым )'
                'и английские буквы в нижнем регистре.',
                code='invalid_color',
            ),
            lowercase_validator,
        ],
    )
    slug = models.CharField(
        'слаг тега',
        max_length=200,
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return leight_field(self.name)


class Ingredient(models.Model):
    """Модель для хранения ингредиентов."""

    name = models.CharField(
        'Название ингредиента', max_length=200)
    measurement_unit = models.CharField(
        'Единица измерения', max_length=200)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return leight_field(self.name)


class Recipe(models.Model):
    """Модель для хранения рецептов."""

    author = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipe',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        through='IngredientInRecipe',
        related_name='recipe',
    )
    tags = models.ManyToManyField(
        Tag, verbose_name='Список тегов',)
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/'
    )
    name = models.CharField('Название рецепта', max_length=200)
    text = models.TextField('Описание рецепта')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[
            MinValueValidator(1, message='Время приготовления должно '
                              'быть не меньше одной минуты'),
            MaxValueValidator(1440, message='Время приготовления не должно '
                              'превышать 1440 минут')
        ]
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return leight_field(self.name)


class IngredientInRecipe(models.Model):
    """Модель для хранения связей между рецептами и ингредиентами."""

    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='ингредиент',
        related_name='ingredient_inrecipe',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='рецепт',
        related_name='ingredient_recipe',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        'Количество ингрединта',
        validators=[
            MinValueValidator(1, 'Значение должно быть не меньше 1'),
            MaxValueValidator(10000, message='Значение не должно быть '
                              'больше 10000')
        ]
    )

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Ингредиент и рецепт'
        verbose_name_plural = 'Ингредиенты и рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='ingredient_in_recipe_unique',
            )
        ]

    def __str__(self):
        return format_string(self.ingredient.name, self.recipe.name)


class Follow(models.Model):
    """Модель с подписками на авторов."""

    user = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )
    date_followed = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('user',)
        verbose_name = 'Избранный автор'
        verbose_name_plural = 'Подписки на авторов'
        unique_together = ('user', 'author')

    def __str__(self):
        return format_string(self.user.username, self.author.username)

    def clean(self):
        if self.user == self.author:
            raise ValidationError('Нельзя подписаться на самого себя.')


class ShopingCartAndFavoriteRecipe(models.Model):
    user = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='Рецепт'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return format_string(self.user.username, self.recipe.name)


class FavoriteRecipe(ShopingCartAndFavoriteRecipe):
    """Модель для хранения избранных рецептов."""

    user = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='favorite_user',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        unique_together = ('user', 'recipe')


class ShopingCart(ShopingCartAndFavoriteRecipe):
    """Модель для хранения корзины."""

    user = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='shoppingcart_user',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoppingcart_recipe',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        unique_together = ('user', 'recipe')
