from celery import shared_task
import requests
from shop.models import Book, Order

@shared_task()
def shelf_check():
    shelf = requests.get('http://127.0.0.1:8001/Book/')
    if shelf.status_code == 200:
        for book in shelf.json():
            Book.objects.update_or_create(title=book['title'],
                                          id_in_store=book['id'],
                                          defaults={'price': book['price'],
                                                    'quantity': len(book['bookitem'])})

@shared_task()
def check_order_status():
    orders = requests.get('http://127.0.0.1:8001/Order/')
    if orders.status_code == 200:
        for order in orders.json():
            if order['status'] == 'Success':
                change = Order.objects.get(pk=order['order_id_in_shop'])
                change.status = 'Success'
                change.save()