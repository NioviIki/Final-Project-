from rest_framework import serializers
from .models import Book, BookItem, OrderBookItem, Order, OrderItem


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'price']