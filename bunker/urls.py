from django.urls import path
from django.views import generic

from . import views

app_name = "bunker"

urlpatterns = [
    # /
    path("", generic.RedirectView.as_view(url='all-orders/')),

    # /all-orders/
    path("all-orders/", views.AllOrders.as_view(), name='all_orders'),

    # /order/34/
    path("order/<int:order_id>/", views.Order.as_view(), name='order'),
]
