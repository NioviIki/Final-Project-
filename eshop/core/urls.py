from django.contrib import admin
from django.urls import include, path
from shop.urls import router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('', include('shop.urls')),
    path('register_order_after_accept/', include(router.urls)),
]
