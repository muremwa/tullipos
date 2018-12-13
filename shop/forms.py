from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.validators import ValidationError

import re

from .models import CustomerOrder


class UserFeedBackForm(forms.Form):
    feedback = forms.CharField(max_length=500, widget=forms.Textarea)
    email = forms.EmailField(widget=forms.EmailInput, help_text='This is required but will never be used')


class CustomerOrderForm(forms.ModelForm):
    class Meta:
        model = CustomerOrder
        fields = ('preferred_name', 'phone_number', 'residence',)

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        if len(data) != 10:
            raise ValidationError(_('The phone number is not valid (not 10 digits)'), code='Less Than 10')

        if not re.search(r'^07\d{8}', data):
            raise ValidationError(_('This is not a valid number'), code='not 07..')

        return data
