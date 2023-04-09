from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, OrderItem, Order
from django.db import models


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = UserProfile
        fields = ["username", "email", "password1", "password2"]



class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity']

class OrderAcceptForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('delivery_adress', )