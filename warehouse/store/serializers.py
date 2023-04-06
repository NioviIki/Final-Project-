from rest_framework import serializers
from .models import Book, BookItem, OrderBookItem, Order, OrderItem


class BookSerializer(serializers.ModelSerializer):
    bookitem = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Book
        fields = ['id', 'title', 'price', 'bookitem']


class BookItemSerializer(serializers.ModelSerializer):
    book = serializers.ReadOnlyField(source='book.title')
    class Meta:
        model = BookItem
        fields = ['book', 'place']


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