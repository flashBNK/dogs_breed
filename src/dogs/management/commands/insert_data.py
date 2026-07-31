from django.core.management.base import BaseCommand
from django.db import transaction

from ...factories import DogFactory

DOGS_COUNT = 20


class Command(BaseCommand):
    help = "Наполняет БД данными о собаках и породах. Безопасна для повторного запуска."

    def handle(self, *args, **options):
        with transaction.atomic():
            for _ in range(DOGS_COUNT):
                DogFactory()
        self.stdout.write(self.style.SUCCESS(f"Готово: создано {DOGS_COUNT} собак (или меньше, в случае совпадений)"))
