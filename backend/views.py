import string
from typing import List
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
                        shipping_address = address_entries[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(self.request, "This default shipping address does not exist")
                        return redirect('core:checkout')
                else:
                    print("Enter a new shipping address")
                    ship_addr1 = form.cleaned_data.get('shipping_address')
                    ship_country = form.cleaned_data.get('shipping_country')
                    ship_zip = form.cleaned_data.get('shipping_zip')

                    shipping_info = [ship_addr1, ship_country, ship_zip]
                    if valid_form(shipping_info):
                        shipping_address = Address(user=self.request.user, street_address=ship_addr1, country=ship_country, zip = ship_zip, address_type='S')
                        shipping_address.save()
                        order.shipping_address = shipping_address
                        order.save()

                        set_def_shipping = form.cleaned_data.get('set_default_shipping')
                        if set_def_shipping:
                            shipping_address.default = shipping_address.save()
                    else:
                        messages.info(self.request, "Please fill in the required shipping address fields")


            use_default_billing = form.cleaned_data.get('use_default_billing')
            identical_bill_address = form.cleaned_data.get('same_billing_address')

            if identical_bill_address:
                bill_addr = shipping_address
                bill_addr.pk = None
                bill_addr.address_type = 'B'
                bill_addr.save()
                order.bill_addr = bill_addr
                order.save()
            
            elif use_default_billing:
                print("Use default billing address")
                address_queries = Address.objects.filter(user=self.request.user, address_type='B', default=True)
                if address_queries.exists():
                    bill_address = address_queries[0]
                    order.bill_address = bill_address
                    order.save()
                else:
                    messages.info(self.request, "This billing address does not exist")
                    return redirect('core:checkout')
            else:
                    print("Enter a new billing address")
                    bill_addr1 = form.cleaned_data.get('shipping_address')
                    bill_country = form.cleaned_data.get('shipping_country')
                    bill_zip = form.cleaned_data.get('shipping_zip')

                    billing_info = [bill_addr1, bill_country, bill_zip]
                    if valid_form(billing_info):
                        billing_address = Address(user=self.request.user, street_address=bill_addr1, country=bill_country, zip = bill_zip, address_type='B')
                        billing_address.save()
                        order.billing_address = billing_address
                        order.save()

                        set_def_billing = form.cleaned_data.get('set_default_billing')
                        if set_def_billing:
                            shipping_address.default = shipping_address.save()
                    else:
                        messages.info(self.request, "Please fill in the required shipping address fields")
                
            payment_choice = form.cleaned_data.get('Payment_Options')

            if payment_choice == Stripe:
                option = Payment_Option.Stripe
            elif payment_choice == PayPal:
                option = Payment_Option.Paypal
            else:
                messages.warning(self.request, "Invalid payment option used")
                return redirect('core:checkout')
            
            return redirect('core:payment', option)

        except ObjectDoesNotExist:
            messages.warning(self.request, "This order does not exist")
            return redirect("core:order-summary")



class HomeDesign(ListView):
    template_name = "home.html"
    model = Item

class ItemSummary(DetailView):
    model = Item
    template_name = "product.html"

class ViewOrder(View, LoginRequiredMixin):
    def obtainOrder(self, *args, **kwargs):
        try:
            context = { 'object': Order.objects.get(user=self.request.user, ordered=False)}
            
            return render(self.request, 'order_summary.html', context)
            
        except ObjectDoesNotExist:
            messages.warning(self.request, "This order does not exist")
            return redirect("/")