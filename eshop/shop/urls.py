from django.urls import path

from . import views

app_name = 'Blog'

urlpatterns = [
    path('', views.BookView.as_view(), name='book'),
    path('profile/<slug:slug>', views.UserProfile.as_view(), name='profile')
]