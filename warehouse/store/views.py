from rest_framework import viewsets

from . import serializers
from .models import Book, BookItem, Order, OrderBookItem, OrderItem


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = serializers.BookSerializer


class BookItemViewSet(viewsets.ModelViewSet):
    queryset = BookItem.objects.filter(orderbookitem__exact=None).order_by('book')
    serializer_class = serializers.BookItemSerializer


class OrderBookItemViewSet(viewsets.ModelViewSet):
    queryset = OrderBookItem.objects.filter(order_item__order__status="In_Work")
    serializer_class = serializers.OrderBookItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.filter(status="In_Work")
    serializer_class = serializers.OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.filter(order__status="In_Work")
    serializer_class = serializers.OrderItemSerializer
