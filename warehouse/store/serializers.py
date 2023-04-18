from rest_framework import serializers

from .models import Book, BookItem, Order, OrderBookItem, OrderItem


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'title', 'price', 'bookitems']


class BookItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookItem
        fields = ['id', 'place', 'book']


class OrderBookItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderBookItem
        fields = ['order_item', 'book_item']


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['url', 'order_id_in_shop', 'user_email', 'status', 'delivery_adress', 'id']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['url', 'order', 'book_title', 'quantity', 'book']
