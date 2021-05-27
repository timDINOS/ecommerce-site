from django import forms
from django.forms.fields import EmailField
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class UserSearchForm(forms.Form):
    user = forms.CharField(required=False)

class UseCoupon(forms.Form):
    coupon_code = forms.CharField(widget=forms.TextInput())

    def apply_coupon(self):
        pass

class OrderItem(forms.Form):
    billing_address = forms.CharField(required=False)
    shipping_address = forms.CharField(required=False)
    