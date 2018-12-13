from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from . import views
from shop import views as shop_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL+"favicon.ico")),

    # faq/
    path('faq/', views.FAQList.as_view(), name="FAQ"),

    # faq/how-do-you-pay/
    path('faq/<slug:slug>/', views.FAQDetail.as_view(), name="FAQ-detail"),

    #
    path('', RedirectView.as_view(url=('shop/')), name='home'),

    # shop/
    path('shop/', include('shop.urls')),

    # search/
    path('search/', shop_views.Search.as_view(), name='search'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




