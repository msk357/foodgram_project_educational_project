# Generated by Django 2.2.16 on 2023-03-06 15:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0003_auto_20230306_1411"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="cooking_time",
            field=models.PositiveSmallIntegerField(
                help_text="Укажите время в минутах",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(500),
                ],
                verbose_name="Время приготовления",
            ),
        ),
    ]
