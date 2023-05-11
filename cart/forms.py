from django import forms

from app.models import Tours
from django.forms import DateInput

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
import re
from django.core.exceptions import ValidationError


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

class CartForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        label='Количество',
        initial=1,
        widget=forms.NumberInput(
            attrs={'class': 'form-control',
                   'style': 'width: 100px; display: inline-block;'}))
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)