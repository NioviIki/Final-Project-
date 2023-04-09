from celery import shared_task
import requests
from shop.models import Book, Order, OrderItem

@shared_task()
def shelf_check():
    shelf = requests.get('http://127.0.0.1:8001/Book/')
    if shelf.status_code == 200:
        for book in shelf.json():
            Book.objects.update_or_create(title=book['title'],
                                          id_in_store=book['id'],
                                          defaults={'price': book['price'],
                                                    'quantity': book['bookitems']})

@shared_task()
def check_order_status():
    orders = requests.get('http://127.0.0.1:8001/Order/')
    if orders.status_code == 200:
        for order in orders.json():
            if order['status'] == 'Success':
                change = Order.objects.get(pk=order['order_id_in_shop'])
                change.status = 'Success'
                change.save()

@shared_task()
def order_check():
    list_of_orders_id_in_store = []
    for order_in_store in requests.get('http://127.0.0.1:8001/Order/').json():
        list_of_orders_id_in_store.append(order_in_store['order_id_in_shop'])
    for order in Order.objects.filter(status='Ordered'):
        if order.id not in list_of_orders_id_in_store:
            myobj = {
                'user_email': order.user_id.email,
                'order_id_in_shop': order.id,
                'status': 'In_Work',
                'delivery_adress': order.delivery_adress
                     }
            requests.post('http://127.0.0.1:8001/Order/', json=myobj)
            for book in OrderItem.objects.filter(order=Order.objects.get(pk=order.id)):
                for i in requests.get('http://127.0.0.1:8001/Order/').json():
                    if i['order_id_in_shop'] == order.id:
                        myobj = {
                            "order": f"http://127.0.0.1:8001/Order/{i['id']}/",
                            "quantity": book.quantity,
                            "book": f'http://127.0.0.1:8001/Book/{Book.objects.get(title=book.book.title).id}/'
                        }
                        requests.post('http://127.0.0.1:8001/OrderItem/', json=myobj)