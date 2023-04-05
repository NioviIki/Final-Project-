from rest_framework import serializers
from .models import Book, BookItem, OrderBookItem, Order, OrderItem


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'price']


class BookItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookItem
        fields = ['book', 'palce']


class OrderBookItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderBookItem
        fields = ['order_item', 'book_item']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user_email', 'status', 'delivery_adress']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'book', 'quantity']