from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    def __str__(self):
        return self.title

class BookItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='bookitem')
    place = models.CharField(max_length=50, blank=True)
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
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    def __str__(self):
        return f'{self.order}: {self.book}'

class OrderBookItem(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    book_item = models.OneToOneField(BookItem, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.order_item}: {self.book_item}'
