from django.contrib import admin

from .models import Shoe, CustomerOrder, ShoeImage, FAQ, Tag


class ImageInline(admin.TabularInline):
    model = ShoeImage
    extra = 3


class ShoeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Shoe details', {'fields': ['name', 'price', 'size', 'color', 'brand', 'sex', 'available']}),
        ('Description', {'fields': ['description', 'rating', 'tags']})
    ]
    list_display = ['name', 'brand', 'color', 'price']
    list_filter = ['brand', 'tags', 'size', 'sex', 'color', 'available']
    search_fields = ['brand', 'sex', 'color', 'size']
    inlines = (ImageInline,)


class CustomerOrderAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Personal info', {'fields': ['preferred_name', 'phone_number', 'residence']}),
        ('Order details', {'fields': ['shoes_ordered', 'cleared', 'cancelled',]})
    ]
    list_display = ('preferred_name', 'residence', 'total_amount', 'cleared', 'cancelled')
    list_filter = ['created', 'cancelled', 'cleared', 'residence']
    search_fields = ['created', 'phone_number', 'preferred_name', 'residence']
    actions = ['mark_as_cleared']

    def mark_as_cleared(self, request, queryset):
        orders = queryset.update(cleared=True)
        if orders == 1:
            count = "1 order "
        else:
            count = "{} orders ".format(orders)
        self.message_user(request, count + "cleared")


class FAQAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question', {'fields': ['question', 'tag']}),
        ('Answer', {'fields': ['answer']})
    ]
    list_filter = ['tag']
    search_fields = ['question', 'tag']


admin.site.register(Shoe, ShoeAdmin)
admin.site.register(CustomerOrder, CustomerOrderAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Tag)
