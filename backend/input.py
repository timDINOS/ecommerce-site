from django import forms
from django.forms.fields import EmailField
from django.forms.widgets import Textarea
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
import enum


class Payment_Options(enum.Enum):
    Stripe = 0
    Paypal = 1

class UserSearchForm(forms.Form):
    user = forms.CharField(required=False)

class UseCoupon(forms.Form):
    coupon_code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))

    def apply_coupon(self):
        pass

class OrderItem(forms.Form):
    billing_address = forms.CharField(required=False)
    shipping_address = forms.CharField(required=False)
    zip_code = forms.CharField(required=False)


class refundForm(forms.Form):
    code_to_refund = forms.CharField()
    send_email_line = forms.CharField(widget=Textarea())
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    email_address = forms.EmailField()


class Payment(forms.Form):
    stripe = forms.CharField(require=False)


class PaymentProcess(forms.Form):
    addr = forms.CharField(required=False)
    sec_addr = forms.CharField(required=False)
    loc = CountryField(blank_label='(selecg country)').formfield(required=False, widget=CountrySelectWidget(attrs={'class': 'custom-select d-block w-100'}))
    zip_code = forms.CharField(required=False)

    bill_addr = forms.CharField(required=False)
    sec_bill_addr = forms.CharField(required=False)
    bill_loc = CountryField(blank_label='(selecg country)').formfield(required=False, widget=CountrySelectWidget(attrs={'class': 'custom-select d-block w-100'}))
    bill_zip_code = forms.CharField(required=False)
    
    set_ship_addr = forms.BooleanField(required=False)
    set_bill_addr = forms.BooleanField(required=False)
    matching_bill_addr = forms.BooleanField(required=False)

    using_shipping_default = False
    using_billing_default = False

    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=Payment_Options.choices)