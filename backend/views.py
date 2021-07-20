import string
import stripe
import random


from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, View

stripe_key = settings.STRIPE_SECRET_KEY

from .input import UserSearchForm, UseCoupon, OrderItem, refundForm, Payment, PaymentProcess
from .models import Item, BuyItem, MakeOrder, AccountProfile, Address, UserGroup, FriendGroup, Coupon

def create_code():
    code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=30))
    return code

def getItems(request):
    return render(request, "products.html", {'items': Item.objects.all()})


def valid_form(values):
    for value in values:
        if field == '':
            return False
    return True

class CheckoutDesign(View):
    def get_order(self, *args, **kwargs):
        try:
            form = PaymentProcess()
            order = OrderItem.objects.get(user=self.request.user, ordered=False)

            context = {
                'form': form,
                'couponform': UseCoupon(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address.exists():
                context.update({'default_shipping_address': shipping_address[0]})
            
            billing_address = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if billing_address.exists():
                context.update({'default_billing_address': billing_address[0]})

            return render(self.request, "checkout.html", context)

        except ObjectDoesNotExist:
            messages.info(self.request, "This order does not exist")
            return redirect("core:checkout")
        

    def post(self, *args, **kwargs):
        form = PaymentProcess(self.request.POST or None)
        try:
            order = OrderItem.objects.get(user=self.request.user, ordered=False)
            valid = form.is_valid()
            if valid:
                def_shipping = form.cleaned_data.get('use_default_shipping')
                if def_shipping:
                    print("Using default address")
                    address_entries = Address.objects.filter(user=self.equest.user, address_type='S', default=True)
                    if address_entries.exists():
                        
        except ObjectDoesNotExist:
            messages.warning(self.request, "This order does not exist")
            return redirect("core:order-summary")