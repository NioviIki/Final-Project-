from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()
class UserProfile(User):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()

    def get_absolute_url(self):
        return reverse("profile", kwargs={"slug": self.slug})

class Book(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    quantity = models.IntegerField()
    id_in_store = models.IntegerField()


class Order(models.Model):
    class Status(models.TextChoices):
        Cart = 'Cart'
        Success = 'Success'
        Fail = 'Fail'
        Ordered = 'Ordered'

    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    status = models.CharField(max_length=7, choices=Status.choices)
    delivery_adress = models.CharField(max_length=50)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()








