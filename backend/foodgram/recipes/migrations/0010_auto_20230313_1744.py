# Generated by Django 2.2.16 on 2023-03-13 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0009_auto_20230313_1442"),
    ]

    operations = [
        migrations.AlterField(
            model_name="amountingredient",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ingredient",
                to="recipes.Recipe",
                verbose_name="В каком рецепте",
            ),
        ),
    ]
