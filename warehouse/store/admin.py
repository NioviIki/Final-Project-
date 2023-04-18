from django.contrib import admin
from django import forms

from .models import Book, BookItem, OrderBookItem


@admin.register(Book)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    list_filter = ['price']
    search_fields = ['title', 'price']
    list_per_page = 20

@admin.register(BookItem)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('book', 'place')
    list_filter = ['book']
    search_fields = ['book', 'place']
    list_per_page = 20

@admin.register(OrderBookItem)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('order_item', 'book_item')
    list_filter = ['order_item']
    search_fields = ['order_item', 'book_item']
    list_per_page = 20

