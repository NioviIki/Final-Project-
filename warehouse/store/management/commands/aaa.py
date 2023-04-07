import random
import requests
from store.models import Book, BookItem, OrderBookItem, Order, OrderItem

from django.core.management import BaseCommand

from faker import Faker


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('aaa', nargs='?',
                            help='Fill in the values')

    def handle(self, *args, **options):
        fake = Faker()

        orders = requests.get('http://127.0.0.1:8000/register_order_after_accept/Order/')
        if orders.status_code == 200:
            for order in orders.json():
                try:
                    Order.objects.get(order_id_in_shop=order['id'])
                except Order.DoesNotExist:
                    Order.objects.create(user_email= order['user_email'],
                                         status='In_Work',
                                         delivery_adress=order['delivery_adress'],
                                         order_id_in_shop=order['id'])
                    for book in order['order_item']:
                        list_sep = book.split()
                        OrderItem.objects.create(order=Order.objects.get(order_id_in_shop=order['id']),
                                                 book=Book.objects.get(title=' '.join(list_sep[:len(list_sep) - 1])),
                                                 quantity=list_sep[-1])
