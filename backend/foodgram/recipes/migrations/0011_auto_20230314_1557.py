# Generated by Django 2.2.16 on 2023-03-14 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0010_auto_20230313_1744"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="in_shopping_cart",
                to="recipes.Recipe",
                verbose_name="Рецепты в корзине",
            ),
        ),
        migrations.AlterField(
            model_name="favorit",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="in_favorites",
                to="recipes.Recipe",
                verbose_name="Избранные рецепты",
            ),
        ),
    ]
