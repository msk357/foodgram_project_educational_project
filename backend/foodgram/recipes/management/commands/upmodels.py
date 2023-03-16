"""Менеджмент команда для добавления данных в БД.
Для добавления данных необходимо:
- Импортировать модель;
- Указать модель в переменной obj;
- Указать поля модели в переменных obj.MyFields;
Для применения команды в консоли прописываем:
  python manage.py upmodels /path/csv.
"""
import csv
from django.core.management.base import BaseCommand
from django.db import connection

from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Загрузка данных из CSV-файлов"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Путь к CSV-файлу")

    def handle(self, *args, **options):
        csv_file = options["csv_file"]
        with open(csv_file, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                obj = Ingredient()
                obj.name = row[0]
                obj.measurement_unit = row[1]
                obj.save()
        connection.cursor().execute("COMMIT;")
