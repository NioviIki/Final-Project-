from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=100, decimal_places=2)

class BookItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    palce = models.CharField(max_length=50, blank=True)



class Order(models.Model):
    class Status(models.TextChoices):
        In_Work = '1'
        Success = '2'
        Fail = '3'

    user_email = models.EmailField()
    status = models.CharField(max_length=3, choices=Status.choices)
    delivery_adress = models.CharField(max_length=50)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class OrderBookItem(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    book_item = models.ForeignKey(BookItem, on_delete=models.CASCADE)
