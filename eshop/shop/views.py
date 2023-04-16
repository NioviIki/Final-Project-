from rest_framework import viewsets

from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import views, get_user_model, authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth import mixins
from django.contrib.messages.views import SuccessMessageMixin

from .serializers import OrderSerializer
from .models import Book, Order, OrderItem, UserProfile
from .forms import RegisterForm, OrderItemForm, OrderAcceptForm


User = get_user_model()


class UserProfileView(generic.DetailView):
    model = UserProfile
    template_name = 'shop/registration/user_detail.html'

    def get_queryset(self):
        return UserProfile.objects.filter(slug=self.kwargs['slug'])



class LoginViewUpdated(views.LoginView):
    template_name = 'shop/registration/login.html'
    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return resolve_url(self.next_page)
        else:
            return resolve_url(reverse_lazy('shop:profile', kwargs={'slug': self.request.user}))


class LogoutViewUpdated(views.LogoutView):
    template_name = 'shop/registration/logout.html'


class RegistrationView(generic.FormView):
    template_name = 'shop/registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy("shop:profile")

    def form_valid(self, form):
        self.success_url = reverse_lazy('shop:profile', kwargs={'slug': form.cleaned_data['username']})
        UserProfile.objects.create(slug=form.cleaned_data['username'],
                                   username=form.cleaned_data['username'],
                                   email=form.cleaned_data['email'],
                                   password=make_password(form.cleaned_data['password1'])
                                   )

        user = authenticate(self.request, username=form.cleaned_data['username'], password=form.cleaned_data.get("password1"))
        login(self.request, user)
        return super().form_valid(form)

class BookView(generic.ListView):
    model = Book
    template_name = 'shop/book_list.html'
    paginate_by = 15

    def get_queryset(self):
        return Book.objects.filter(quantity__gt=0)

class OrderItemView(mixins.LoginRequiredMixin, SuccessMessageMixin, generic.FormView):
    form_class = OrderItemForm
    template_name = 'shop/order_item.html'
    success_message = 'Accepted'
    login_url = reverse_lazy('shop:login')

    def form_valid(self, form):
        Order.objects.filter(status='Cart').get_or_create(user_id=UserProfile.objects.get(slug=self.request.user),
                                                                defaults={'status': 'Cart'})
        try:
            OrderItem.objects.create(order=Order.objects.filter(status='Cart').get(user_id=UserProfile.objects.get(slug=self.request.user)),
                                     book=Book.objects.filter(quantity__gt=0).get(pk=self.kwargs['pk']),
                                     quantity=form.cleaned_data['quantity']
                                     )
        except Book.DoesNotExist:
            self.success_url = reverse_lazy('shop:book')
            return super().form_valid(form)

        self.success_url = reverse_lazy('shop:order', kwargs={'pk': self.kwargs['pk']})
        return super().form_valid(form)


class OrderDetail(generic.ListView):
    model = UserProfile
    template_name = 'shop/order_detail.html'

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(status='Cart').get(user_id=UserProfile.objects.get(username=user))



class OrderAccept(generic.FormView):
    form_class = OrderAcceptForm
    template_name = 'shop/order_accept.html'
    success_url = reverse_lazy('shop:book')
    def form_valid(self, form):
        Order.objects.filter(status='Cart', user_id=UserProfile.objects.get(username=self.request.user)).update(
            status='Ordered', delivery_adress=form.cleaned_data['delivery_adress'])

        return super().form_valid(form)

class OrderDelete(generic.DeleteView):
    model = OrderItem
    template_name = 'shop/order_delete.html'
    success_url = reverse_lazy('shop:order_detail')

class OrderUpdate(generic.UpdateView):
    model = OrderItem
    fields = ('quantity', )
    template_name = 'shop/order_update.html'
    success_url = reverse_lazy('shop:order_detail')


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.filter(status='Ordered')
    serializer_class = OrderSerializer