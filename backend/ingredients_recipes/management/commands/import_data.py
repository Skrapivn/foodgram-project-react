import csv

from django.core.management.base import BaseCommand, CommandError

from ingredients_recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Import Ingredients'

    def handle(self, *args, **options):
        try:
            with open(
                'ingredients_recipes/data/ingredients.csv',
                 encoding="utf8") as file:
                file_reader = csv.reader(file)
                for row in file_reader:
                    name, measurement_unit = row
                    Ingredient.objects.get_or_create(
                        name=name, measurement_unit=measurement_unit)
                self.stdout.write(self.style.SUCCESS(
                    'Ingredient import - success'))
        except Exception:
            raise CommandError(
                'Файл не найден или возникла ошибка при обработке ингредиентов'
            )
