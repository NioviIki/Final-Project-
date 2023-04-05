from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    def __str__(self):
        return self.title

class BookItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    palce = models.CharField(max_length=50, blank=True)
    def __str__(self):
        return self.book.title


class Order(models.Model):
    class Status(models.TextChoices):
        In_Work = 'In_Work'
        Success = 'Success'
        Fail = 'Fail'

    user_email = models.EmailField()
    status = models.CharField(max_length=7, choices=Status.choices)
    delivery_adress = models.CharField(max_length=50)
    def __str__(self):
        return self.status



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    def __str__(self):
        return f'{self.order}: {self.book}'

class OrderBookItem(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    book_item = models.ForeignKey(BookItem, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.order_item}: {self.book_item}'
