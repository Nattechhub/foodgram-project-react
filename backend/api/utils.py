from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from recipes.models import (IngredientInRecipe, Ingredient, Recipe)


def add_del_recipesview(request, model, recipeminifiedserializer, **kwargs):
    """
    Утилита для view функции recipes. Применяется для:
    Добавить или удалить рецепт в избранных у пользователя.
    Добавить или удалить рецепт из списка покупок.
    """
    recipe_id = kwargs['pk']
    user = request.user
    recipe_obj = get_object_or_404(Recipe, pk=recipe_id)
    data = {
        "id": recipe_id,
        "name": recipe_obj.name,
        "image": recipe_obj.image,
        "cooking_time": recipe_obj.cooking_time,
    }

    if request.method == 'POST':
        serializer = recipeminifiedserializer(
            instance=data,
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            model.objects.create(
                user=user, recipe_id=recipe_id
            )
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )

    if request.method == 'DELETE':
        get_object_or_404(
            model,
            user=user,
            recipe_id=recipe_id
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


def create_update_recipes(validated_data, author=None, instance=None):
    """Утилита для RecipesSerializer для методов create, update."""
    tags = validated_data.pop('tags')
    ingredients = validated_data.pop('ingredientin_recipe')

    if instance is None:
        recipe = Recipe.objects.create(author=author, **validated_data)
    else:
        recipe = instance

    recipe.tags.set(tags)

    IngredientInRecipe.objects.bulk_create([
        IngredientInRecipe(
            recipe=recipe,
            amount=ingredient.get('amount'),
            ingredient=Ingredient.objects.get(
                id=ingredient.get('id')
            ),
        ) for ingredient in ingredients
    ])

    return recipe
