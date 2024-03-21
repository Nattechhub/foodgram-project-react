from django.db import models
from django.core.exceptions import ValidationError


from users.models import FoodgramUser


def leight_field(field):
    if len(field) > 20:
        return field[:20] + '...'
    else:
        return field


class Tag(models.Model):
    """Модель для хранения тегов."""

    name = models.CharField('Название тега', max_length=200)
    color = models.CharField(
        'Цвет тега',
        unique=True,
        max_length=7,
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
    cooking_time = models.PositiveSmallIntegerField('Время приготовления')

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
    amount = models.PositiveSmallIntegerField('Количество ингрединта')

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
        return f'{self.ingredient.name} - {self.recipe.name}'


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
        return f'{self.user.username} - {self.author.username}'

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
        return f'{self.user.username} - {self.recipe.name}'


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
