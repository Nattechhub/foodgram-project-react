from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import (
    Tag, Ingredient, Recipe, FavoriteRecipe,
    Follow, ShopingCart, IngredientInRecipe
)

from import_export import resources
from import_export.admin import ImportExportModelAdmin


class IngredientResource(resources.ModelResource):

    class Meta:
        model = Ingredient


class IngredientAdmin(ImportExportModelAdmin):
    resource_classes = [IngredientResource]


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInRecipeInline,)
    filter_horizontal = ['tags']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def response_add(self, request, obj, post_url_continue=None):
        if not obj.ingredients.exists():
            raise ValidationError(
                'Необходимо добавить хотя бы один ингредиент.')
        return super().response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        if not obj.ingredients.exists():
            raise ValidationError(
                'Необходимо добавить хотя бы один ингредиент.')
        return super().response_change(request, obj)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(FavoriteRecipe)
admin.site.register(Follow)
admin.site.register(ShopingCart)
admin.site.register(IngredientInRecipe)
admin.site.register(Ingredient, IngredientAdmin)
