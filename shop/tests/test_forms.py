from django.test import SimpleTestCase, tag

from ..forms import CustomerOrderForm


@tag('shop-forms')
class ShopFormsTestCase(SimpleTestCase):
    def number_test(self, data, correct, **kwargs):
        form = CustomerOrderForm(data=data)
        if correct:
            self.assertTrue(form.is_valid())
        else:
            self.assertFalse(form.is_valid())
            self.assertEqual(form.errors['phone_number'][0], kwargs['error_message'])

    @tag('phone-number')
    def test_phone_number(self):
        print('Testing phone number')
        numbers = {
            'start': '8940094398',
            'enough': '0723897',
            'more': '0789348934894',
            'mix': '0723hf8938',
            'correct': '0792678654'
        }
        data = []

        for label, num in numbers.items():
            wrong_data = {
                'preferred_name': 'Alice',
                'phone_number': '{}'.format(num),
                'residence': 'Testing Zone'
            }
            data.append(wrong_data)
        x = 'The phone number is not valid (not 10 digits)'
        y = 'This is not a valid number'
        z = 'Ensure this value has at most 10 characters (it has 13).'

        # does not start with 07
        self.number_test(data[0], False, error_message=y)

        # digits do not add up to 10
        self.number_test(data[1], False, error_message=x)

        # more than 10 digits
        self.number_test(data[2], False, error_message=z)

        # mixes digits and letter
        self.number_test(data[3], False, error_message=y)

        # correct number
        self.number_test(data[4], True)
