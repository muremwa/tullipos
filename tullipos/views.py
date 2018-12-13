from django.views import generic

from shop.models import FAQ


# list of all FAQs
class FAQList(generic.ListView):
    model = FAQ
    template_name = 'home/faq_list.html'
    template_name_suffix = '_list'
    context_object_name = 'questions'
    paginate_by = 10


# Each FAQ
class FAQDetail(generic.DetailView):
    model = FAQ
    template_name = 'home/faq_detail.html'
    context_object_name = 'faq'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
