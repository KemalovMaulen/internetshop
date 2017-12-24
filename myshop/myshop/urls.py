
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^', include('shop.urls', namespace='shop')),
    url(r'^order/', include('orders.urls', namespace='orders')),
    url(r'^cupons/', include('cupons.urls', namespace='cupon')),

]

