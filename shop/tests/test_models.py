from django.test import TestCase, tag

from ..models import Shoe, FAQ


class ShopModelTestCase(TestCase):
    @tag('shoe-slug')
    def test_shoe_slug(self):
        shoe = Shoe(
            name='Truck Fit Pro',
            size=5,
            color='gery',
            brand='jk',
            sex='M',
            description='testing a shoe!'
        )
        shoe.save()
        self.assertEqual(shoe.slug, 'truck-fit-pro')

    @tag('faq-slug')
    def test_faq_slug(self):
        faq = FAQ(
            question='This is a Test Question',
            answer='This is a test answer'
        )
        faq.save()
        self.assertEqual(faq.slug, 'this-is-a-test-question')
