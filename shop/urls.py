from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [

    # shop/
    path('', views.ShopIndex.as_view(), name='index'),

    # shop/daemon-balenciaga/
    path('shoe/<slug:slug>/', views.ShoeDetail.as_view(), name='shoe'),

    # /shop/order/
    path('order/', views.CustomerOrdering.as_view(), name='order'),

    # /shop/cart/add/shoe/ | shop/cart/remove/shoe/
    path('shop/cart/<option>/<slug:slug>/', views.CartOptions.as_view(), name='cart-options'),

]
