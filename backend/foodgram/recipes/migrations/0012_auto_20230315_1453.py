# Generated by Django 2.2.16 on 2023-03-15 14:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0011_auto_20230314_1557"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="image",
            field=models.ImageField(
                help_text="Добавьте картинку",
                upload_to="static/",
                verbose_name="Картинка",
            ),
        ),
    ]
