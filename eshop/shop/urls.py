from django.urls import path

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'Order', views.OrderViewSet)

app_name = 'shop'

urlpatterns = [
    path('', views.BookView.as_view(), name='book'),
    path('<int:pk>/', views.OrderItemView.as_view(), name='order'),
    path('order_accept/', views.OrderAccept.as_view(), name='order_accept'),
    path('order_detail/', views.OrderDetail.as_view(), name='order_detail'),
    path('order_delete/<int:pk>', views.OrderDelete.as_view(), name='order_delete'),
    path('order_update/<int:pk>', views.OrderUpdate.as_view(), name='order_update'),

    path('profile/', views.LoginViewUpdated.as_view(), name='login'),
    path('profile/<slug:slug>/', views.UserProfileView.as_view(), name='profile'),
    path('logout/', views.LogoutViewUpdated.as_view(), name='logout'),
    path('register/', views.RegistrationView.as_view(), name='registration'),
]
