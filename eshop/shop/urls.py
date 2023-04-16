from django.urls import path, reverse_lazy
from . import views
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

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


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)