import random

from store.models import Book, BookItem, OrderBookItem, Order, OrderItem

from django.core.management import BaseCommand

from faker import Faker


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('Fill_in_the_values', nargs='?',
                            help='Fill in the values')

    def handle(self, *args, **options):
        fake = Faker()
        for _ in range(3):
            Book.objects.create(title=" ".join(fake.words()), price=random.randint(101, 10000)/100)

        for _ in range(5):
            BookItem.objects.create(place=" ".join(fake.words(2)), book=Book.objects.get(pk=random.randint(1, Book.objects.count())))

