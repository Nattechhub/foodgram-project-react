# Generated by Django 3.2 on 2024-03-21 22:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientinrecipe',
            name='amount',
            field=models.PositiveSmallIntegerField(verbose_name='Количество ингрединта'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(verbose_name='Время приготовления'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, unique=True, verbose_name='Цвет тега'),
        ),
        migrations.AlterUniqueTogether(
            name='favoriterecipe',
            unique_together={('user', 'recipe')},
        ),
        migrations.AlterUniqueTogether(
            name='shopingcart',
            unique_together={('user', 'recipe')},
        ),
    ]
