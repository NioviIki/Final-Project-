from rest_framework import viewsets

from .models import Book, BookItem, OrderBookItem, Order, OrderItem
from .serializers import BookSerializer, BookItemSerializer, OrderBookItemSerializer, OrderSerializer, OrderItemSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookItemViewSet(viewsets.ModelViewSet):
    queryset = BookItem.objects.filter(orderbookitem__exact=None).order_by('book')
    serializer_class = BookItemSerializer


class OrderBookItemViewSet(viewsets.ModelViewSet):
    queryset = OrderBookItem.objects.all()
    # filter(book_item__book__exact=None)
    serializer_class = OrderBookItemSerializer

    # def perform_create(self, serializer):
    #     print(serializer['data'])
    #     pass


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.filter(status="In_Work")
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.filter(order__status="In_Work")
    serializer_class = OrderItemSerializer

