import csv

from django.core.management.base import BaseCommand, CommandError

from ingredients_recipes.models import Tag


class Command(BaseCommand):
    help = 'Import Tags'

    def handle(self, *args, **options):
        try:
            with open(
                'ingredients_recipes/data/tags.csv',
                 encoding="utf8") as file:
                file_reader = csv.reader(file)
                for row in file_reader:
                    name, color, slug = row
                    Tag.objects.get_or_create(
                        name=name, color=color, slug=slug)
                self.stdout.write(self.style.SUCCESS('Tag import - success'))
        except Exception:
            raise CommandError(
                'Файл не найден или возникла ошибка при обработке тегов'
            )
