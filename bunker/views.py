from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import Http404

from shop.models import CustomerOrder


class AllOrders(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_staff:
            raise Http404

        orders = CustomerOrder.objects.order_by('-created')
        return render(self.request, 'bunker/all_orders.html', {
            'orders': orders,
        })


class Order(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_staff:
            raise Http404

        order = get_object_or_404(CustomerOrder, pk=kwargs['order_id'])
        return render(self.request, 'bunker/order.html', {
            'order': order,
        })
