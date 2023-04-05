from django.views import generic
from .models import Book, Order, OrderItem, UserProfile

class BookView(generic.ListView):
    paginate_by = 20
    http_method_names = ["get"]
    model = Book
    template_name = 'shop/book_list.html'

class UserProfile(generic.DetailView):
    http_method_names = ["get"]
    model = UserProfile
    template_name = 'shop/user_detail.html'
