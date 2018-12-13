from django.db import models
from django.urls import reverse
from django.utils.text import slugify

import re


def slug_processor(slug):
    return "-".join(slug.split(" ")).lower()


class Tag(models.Model):
    name = models.CharField(max_length=20)
    for_shoe = models.BooleanField(default=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class ShoeManager(models.Manager):
    @staticmethod
    def get_brands():
        shoes = Shoe.objects.all()
        brands = []
        for shoe in shoes:
            if shoe.brand not in brands:
                brands.append(shoe.brand)
        return brands

    def get_filtered_brands(self, term):
        all_brands = self.get_brands()
        filtered_brands = []

        for brand in all_brands:
            if re.search(r'{}'.format(term), brand, re.M | re.I):
                filtered_brands.append(brand)

        return filtered_brands


class Shoe(models.Model):
    genders = (('M', 'male'), ('F', 'female'), ('U', 'unisex'))
    name = models.CharField(max_length=50)
    slug = models.SlugField(
        help_text="how do you want the url to appear don't edit. An automatic one is generated from name",
        blank=True
    )
    size = models.IntegerField()
    color = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    sex = models.CharField(max_length=2, choices=genders)
    available = models.BooleanField(default=True)
    rating = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)
    description = models.TextField(blank=True)
    price = models.BigIntegerField(default=0.00)
    objects = ShoeManager()

    class Meta:
        ordering = ['-id']

    def save(self, *args, **kwargs):
        self.slug = slug_processor(str(self.name))
        return super().save(args, kwargs)

    def get_absolute_url(self):
        return reverse('shop:shoe', args=[self.slug])

    def get_sex(self):
        if self.sex == "M":
            return self.genders[0][-1]
        elif self.sex == "F":
            return self.genders[1][-1]
        else:
            return self.genders[-1][-1]

    def get_main_image(self):
        return self.shoeimage_set.filter(main=True)[0]

    def __str__(self):
        return self.name


class ShoeImage(models.Model):
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(
        upload_to="shoes/",
        help_text='please make sure the image is in a ratio of 16:9'
    )
    description = models.TextField()
    main = models.BooleanField(
        default=False,
        help_text='Mark at-least one as main(important)'
    )
    objects = models.Manager()

    def __str__(self):
        return "Image for {}".format(self.shoe)


class CustomerOrder(models.Model):
    preferred_name = models.CharField(max_length=50, help_text='Enter the name you would like us to refer to you by')
    phone_number = models.CharField(max_length=10, help_text='Enter a valid Kenyan number starting with \'07\'')
    residence = models.CharField(max_length=50, help_text='Where would you like to get your order')
    shoes_ordered = models.ManyToManyField(Shoe)
    cleared = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    session_id = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('shop:order', args=[str(self.id)])

    def __str__(self):
        return "Order by {}".format(self.preferred_name)


class FAQ(models.Model):
    question = models.CharField(max_length=400)
    slug = models.SlugField(blank=True)
    answer = models.TextField()
    tag = models.ManyToManyField(Tag)
    objects = models.Manager()

    class Meta:
        ordering = ['-id']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.question)
        return super().save(args, kwargs)

    def get_absolute_url(self):
        return reverse('FAQ-detail', args=[self.slug])

    def __str__(self):
        return self.question
