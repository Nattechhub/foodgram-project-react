from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

from recipes.models import FavoriteRecipe, Ingredient, Recipe, ShopingCart, Tag


class IngredientsFilter(filters.FilterSet):
    """
    Фильтрация ингредиентов по полю 'name'
    регистронезависимо, по вхождению в начало названия.
    """
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )
    is_subscribed = filters.BooleanFilter(
        method='filter_is_subscribed'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user

        if FavoriteRecipe.objects.filter(user=user).exists():
            return queryset.filter(favorite_recipe__user=user)

        return queryset.none()

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user

        if ShopingCart.objects.filter(user=user).exists():
            return queryset.filter(shoppingcart_recipe__user=user)

        return queryset.none()

    def filter_is_subscribed(self, queryset, name, value):
        user = self.request.user
        return queryset.filter(author=user)


class RecipeOrderingFilter(OrderingFilter):
    def get_default_ordering(self, view):
        """
        Определяет значение сортировки по умолчанию.
        Сортировка по убыванию ID.
        """
        return ['-id']
