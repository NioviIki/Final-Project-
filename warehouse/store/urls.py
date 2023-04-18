from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'Book', views.BookViewSet)
router.register(r'BookItem', views.BookItemViewSet)
router.register(r'OrderBookItem', views.OrderBookItemViewSet)
router.register(r'Order', views.OrderViewSet)
router.register(r'OrderItem', views.OrderItemViewSet)
