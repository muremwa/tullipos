from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q

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


class BunkerSearch(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_staff:
            raise Http404
        
        try:
            query_term = self.request.GET['query']
        except MultiValueDictKeyError:
            query_term = ''


        q_set = (
            Q(preferred_name__icontains=query_term) |
            Q(phone_number__icontains=query_term) |
            Q(residence__icontains=query_term)
        )

        orders = CustomerOrder.objects.filter(q_set)

        return render(self.request, 'bunker/all_orders.html', {
            'search': True,
            'query': query_term,
            'orders': orders,
        })



















