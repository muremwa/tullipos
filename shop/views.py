from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import View, generic
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist, Q

from .models import Shoe, Tag, FAQ
from .forms import CustomerOrderForm

import re


# all shoes
class ShopIndex(generic.ListView):
    model = Shoe
    template_name = 'shop/shoe_list.html'
    context_object_name = 'shoes'
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['brands'] = Shoe.objects.get_brands()[:5]
        try:
            context['cart'] = self.request.session['cart']
        except KeyError:
            self.request.session['cart'] = []
            context['cart'] = self.request.session['cart']
        context['tags'] = Tag.objects.filter(for_shoe=True)[:3]
        return context


# each shoe
class ShoeDetail(generic.DetailView):
    model = Shoe
    template_name = 'shop/shoe.html'
    context_object_name = 'shoe'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        try:
            liked = self.request.session['liked_brands']
            liked.append(context['shoe'].brand)
            self.request.session['liked_brands'] = liked
        except KeyError:
            self.request.session['liked_brands'] = []
            self.request.session['liked_brands'].append(context['shoe'].brand)
        context['shoes'] = Shoe.objects.all()
        context['cart'] = self.request.session['cart']
        if context['shoe'].id in context['cart']:
            context['in_cart'] = True
        else:
            context['in_cart'] = False
        return context


# customer ordering
class CustomerOrdering(View):
    form = CustomerOrderForm
    template_name = 'shop/order.html'

    @staticmethod
    def get_shoes_in_cart(list_):
        _list = []
        for i in list_:
            try:
                _list.append(Shoe.objects.get(pk=i))
            except ObjectDoesNotExist:
                continue
        return _list

    def get(self, request):
        try:
            cart_ = request.session['cart']
        except KeyError:
            request.session['cart'] = []
            cart_ = request.session['cart']

        cart = self.get_shoes_in_cart(cart_)

        return render(request, self.template_name, {
            'form': CustomerOrderForm,
            'cart': cart
        })

    def post(self, request):
        form = CustomerOrderForm(request.POST)
        shoe_list = request.session['cart']
        if form.is_valid():
            form.save()
            for i in shoe_list:
                try:
                    shoe = Shoe.objects.get(id=i)
                    shoe.available = False
                    shoe.save()
                    form.instance.shoes_ordered.add(shoe)
                except ObjectDoesNotExist:
                    continue
            if len(form.instance.shoes_ordered.all()) < 1:
                form.instance.delete()
                return redirect(reverse('shop:order'))
            request.session['cart'] = []
        else:
            return render(request, self.template_name, {
                'form': form,
                'cart': self.get_shoes_in_cart(shoe_list)
            })

        return render(request, self.template_name, {
            'post_post': True,
        })


# cart options
class CartOptions(View):
    @staticmethod
    def post(request, **kwargs):
        response = dict()
        cart = request.session['cart']
        shoe = get_object_or_404(Shoe, slug=kwargs['slug'])

        if kwargs['option'] == 'add':
            if shoe.id not in cart:
                cart.append(shoe.id)
            request.session['cart'] = cart
            response = {'success': True, 'message': '{} added to cart'.format(shoe.name)}

        elif kwargs['option'] == 'remove':
            cart.remove(shoe.id)
            request.session['cart'] = cart
            response = {'success': True, 'message': '{} removed from cart'.format(shoe.name)}

        else:
            response['success'] = False
            response['text'] = '{} is not supported'

        return JsonResponse(response)


class Search(generic.TemplateView):
    template_name = 'shop/search.html'
    males = ['M', 'MALE', 'MALES', 'MEN', 'BOYS', 'BOY']
    females = ['F', 'FEMALE', 'FEMALES', 'WOMEN', 'GIRLS', 'GIRL']
    tag_names = ['SPORT', 'CASUAL', 'OFFICIAL', 'PARTY']

    def search_shoes(self, term):
        q_set_shoes = (
            Q(name__icontains=term) |
            Q(brand__icontains=term) |
            Q(tags__name__icontains=term)
        )

        return {
            'shoes': Shoe.objects.filter(q_set_shoes),
            'brands': Shoe.objects.get_filtered_brands(term),
            'faq': FAQ.objects.filter(question__icontains=term)
        }

    def master_search(self, query):
        results = dict()
        special_search_feature = None

        # if a key key is added to search term 'brand:nike' extract key and make search special
        if re.search(r'\w+:\w+', query, re.M | re.I):
            special_search = True
            special_search_feature = re.findall(r'\w+', query, re.M | re.I)[0]
            query_term = re.findall(r':\w+', query, re.M | re.I)[0].split(':')[-1]
            print(special_search_feature)

        # if not key make a normal search
        else:
            special_search = False
            query_term = query

        # special search
        if special_search:
            if special_search_feature == 'brand':
                results['shoes'] = Shoe.objects.filter(brand__icontains=query_term)
                results['brands'] = Shoe.objects.get_filtered_brands(query_term)

            elif special_search_feature == 'color':
                results['shoes'] = Shoe.objects.filter(color=query_term)

            elif special_search_feature == 'faq':
                results['faq'] = FAQ.objects.filter(question__icontains=query_term)

            elif special_search_feature == 'size':
                results['shoes'] = Shoe.objects.filter(size=int(query_term))

            elif special_search_feature == 'price':
                pass

            elif special_search_feature == 'sex' or special_search_feature == 'gender':
                key = None
                if query_term.upper() in self.males:
                    key = 'M'
                elif query_term.upper() in self.females:
                    key = 'F'
                elif query_term.upper() == 'ALL' or query_term.upper() == 'UNISEX':
                    key = 'U'

                results['shoes'] = Shoe.objects.filter(sex=key)

            elif special_search_feature == 'tag':
                tags = Tag.objects.filter(name__icontains=query_term)
                results['shoes'] = Shoe.objects.filter(tags__name__icontains=query_term)
                results['faq'] = FAQ.objects.filter(tag__name__icontains=query_term)

            else:
                results['message'] = 'No such filter as {}'.format(special_search_feature)

            results['feature'] = special_search_feature
            results['term'] = query_term

        # normal search
        else:
            results = self.search_shoes(query_term)

        return results

    def get(self, request, *args, **kwargs):
        raw_query = request.GET['query']
        results = self.master_search(raw_query)

        return render(request, self.template_name, {
            'results': results,
            'cart': request.session['cart'],
            'query': raw_query
        })
