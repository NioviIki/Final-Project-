from rest_framework import serializers
from .models import Book, BookItem, OrderBookItem, Order, OrderItem


class BookSerializer(serializers.ModelSerializer):
    # bookitem = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Book
        fields = ['id', 'title', 'price', 'bookitems']


class BookItemSerializer(serializers.ModelSerializer):
    # book = serializers.
    class Meta:
        model = BookItem
        fields = ['place', 'book']


class OrderBookItemSerializer(serializers.ModelSerializer):
    book_items = serializers.StringRelatedField(many=False, source='book_item', read_only=False)
    class Meta:
        model = OrderBookItem
        fields = ['order_item', 'book_items']


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['url', 'order_id_in_shop', 'user_email', 'status', 'delivery_adress', 'id']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['url', 'order', 'book_title', 'quantity', 'book']