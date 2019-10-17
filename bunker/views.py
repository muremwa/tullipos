from django.views import View
from django.shortcuts import render

from shop.models import CustomerOrder


class AllOrders(View):
    def get(self, *args, **kwargs):
        orders = CustomerOrder.objects.order_by('-created')
        return render(self.request, 'bunker/all_orders.html', {
            'orders': orders
        })


class Order(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'bunker/order.html')
