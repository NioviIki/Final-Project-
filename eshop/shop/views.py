from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, views
from django.contrib.auth import mixins
from django.contrib.auth.hashers import make_password
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.views import generic

from rest_framework import viewsets

from .forms import OrderAcceptForm, OrderItemForm, RegisterForm
from .models import Book, Order, OrderItem, UserProfile
from .serializers import OrderSerializer


User = get_user_model()


class UserProfileView(generic.DetailView):
    model = UserProfile
    template_name = 'shop/registration/user_detail.html'

    def get_queryset(self):
        return UserProfile.objects.filter(slug=self.kwargs['slug'])


class LoginViewUpdated(views.LoginView):
    template_name = 'shop/registration/login.html'

    def get_default_redirect_url(self):
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
        self.success_url = reverse_lazy(
            'shop:profile',
            kwargs={'slug': form.cleaned_data['username']}
        )
        UserProfile.objects.create(slug=form.cleaned_data['username'],
                                   username=form.cleaned_data['username'],
                                   email=form.cleaned_data['email'],
                                   password=make_password(form.cleaned_data['password1'])
                                   )

        user = authenticate(
            self.request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data.get("password1")
        )
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

    def post(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(slug=self.request.user)
        Order.objects.filter(status='Cart').get_or_create(
            user_id=user_profile,
            defaults={'status': 'Cart'}
        )
        form = self.get_form()
        pk_kw = self.kwargs['pk']
        if form.is_valid() and form.cleaned_data['quantity'] <= Book.objects.get(pk=pk_kw).quantity:
            try:
                OrderItem.objects.get(
                    order=Order.objects.filter(status='Cart').get(user_id=user_profile),
                    book=Book.objects.get(pk=pk_kw)
                )
            except OrderItem.DoesNotExist:
                return self.form_valid(form)
            else:
                if OrderItem.objects.get(
                        order=Order.objects.filter(status='Cart').get(user_id=user_profile),
                        book=Book.objects.get(pk=pk_kw)
                ).quantity < Book.objects.get(pk=pk_kw).quantity:
                    return self.form_valid(form)
                return self.form_invalid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(
            form=form,
            error_messages='not Accepted')
        )

    def form_valid(self, form):
        user_profile = UserProfile.objects.get(slug=self.request.user)
        pk_kw = self.kwargs['pk']
        try:
            try:
                x = OrderItem.objects.get(
                    order=Order.objects.filter(status='Cart').get(user_id=user_profile),
                    book=Book.objects.filter(quantity__gt=0).get(pk=pk_kw),
                )
            except OrderItem.DoesNotExist:
                OrderItem.objects.create(
                    order=Order.objects.filter(status='Cart').get(user_id=user_profile),
                    book=Book.objects.filter(quantity__gt=0).get(pk=pk_kw),
                    quantity=form.cleaned_data['quantity']
                    )
            else:
                OrderItem.objects.filter(
                    order=Order.objects.filter(status='Cart').get(user_id=user_profile),
                    book=Book.objects.filter(quantity__gt=0).get(pk=pk_kw),
                ).update(quantity=x.quantity + form.cleaned_data['quantity'])

        except Book.DoesNotExist:
            self.success_url = reverse_lazy('shop:book')
            return super().form_valid(form)

        self.success_url = reverse_lazy('shop:order', kwargs={'pk': pk_kw})
        return super().form_valid(form)


class OrderDetail(mixins.LoginRequiredMixin, generic.ListView):
    model = UserProfile
    template_name = 'shop/order_detail.html'
    login_url = reverse_lazy('shop:login')

    def get_queryset(self):
        user = self.request.user
        try:
            Order.objects.get(status='Cart', user_id=UserProfile.objects.get(username=user))
        except Order.DoesNotExist:
            return messages.error(self.request, 'Your shopping cart is empty')
        else:
            if Order.objects.filter(status='Cart').annotate(
                sum_of_order=Sum('order_item__book__price') * Sum('order_item__quantity'),
                quantity_of_order=Sum('order_item__quantity')
            ).get(user_id=UserProfile.objects.get(username=user)).order_item.all():

                return Order.objects.filter(status='Cart').annotate(
                    sum_order=Sum('order_item__book__price') * Sum('order_item__quantity'),
                    quantity_of_order=Sum('order_item__quantity')
                ).get(user_id=UserProfile.objects.get(username=user))
            else:
                return messages.error(self.request, 'Your shopping cart is empty')


class OrderAccept(generic.FormView):
    form_class = OrderAcceptForm
    template_name = 'shop/order_accept.html'
    success_url = reverse_lazy('shop:book')

    def form_valid(self, form):
        Order.objects.filter(status='Cart',
                             user_id=UserProfile.objects.get(
                                 username=self.request.user)).update(
            status='Ordered', delivery_adress=form.cleaned_data['delivery_adress'])

        return super().form_valid(form)


class OrderDelete(generic.DeleteView):
    model = OrderItem
    template_name = 'shop/order_delete.html'
    success_url = reverse_lazy('shop:order_detail')


class OrderUpdate(generic.UpdateView):
    model = OrderItem
    form_class = OrderItemForm
    template_name = 'shop/order_update.html'
    success_url = reverse_lazy('shop:order_detail')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid() and form.cleaned_data['quantity'] <= Book.objects.get(
                pk=OrderItem.objects.get(
                    pk=self.kwargs['pk']).book_id).quantity:
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form,
                                                             error_messages='not Accepted'))


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.filter(status='Ordered')
    serializer_class = OrderSerializer
