from django.contrib import admin

from .models import FoodgramUser


class FoodgramUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'status', "password")
    list_filter = ('username', 'email',)
    search_fields = ('username', 'email',)
    empty_value_display = '-пусто-'


admin.site.register(FoodgramUser, FoodgramUserAdmin)
