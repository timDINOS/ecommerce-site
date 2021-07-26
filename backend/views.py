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
from .models import Item, BuyItem, MakeOrder, AccountProfile, Address, UserGroup, FriendGroup, Coupon, Refund

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


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = OrderItem.objects.get(user=self.request.user, ordered=False)
        if order.billing_address == True:
            profile = self.request.user.profile
            if profile.purchasing == True:
                card_numbers = stripe.Customer.list_sources(profile.stripe_customer_id, limit=10, object="card_numbers")
                cards = cards['data']
            return render(self.request, "payment.html", {'order': order, 'DISPLAY_COUPON_FORM': False, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY, 'card': card_numbers[0]})
        else:
            messages.info(self.request, "This billing address is not recognized")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        order = BuyItem.objects.get(user=self.request.user, ordered=False)
        PayForm = PaymentProcess(self.request.POST)
        profile = AccountProfile.objects.get(user=self.request.user)
        if PayForm.is_valid():
            token = PayForm.cleaned_data.get('stripeToken')
            save_info = PayForm.cleaned_data.get('save')
            default = PayForm.cleaned_data.get('use_default')

            if save_info:
                if profile.stripe_customer_id and profile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(profile.stripe_customer_id)
                    customer.sources.create(source=token)
                else:
                    customer = stripe.Customer.create(email=self.request.user.email)
                    customer.sources.create(source=token)
                    profile.stripe_customer_id = customer["id"]
                    profile.purchasing = True
                    profile.save()
            
            amount_spent = order.get_official_price()

            try:
                source = ""
                if default or save:
                    source = profile.stripe_customer_id
                else:
                    source = token
                charge = stripe.Charge.create(amount=amount_spent, currency="usd", source=source)

                payment = Payment()
                payment.user = self.request.user
                payment.amount = order.get_official_price()
                payment.stripe_charge_id = charge["id"]
                payment.save()

                ordered_items = order.items.all()
                ordered_items.update(ordered=True)
                for ordered_item in ordered_items:
                    ordered_item.save()

                order.payment = payment
                order.code = create_code()
                order.ordered = True
                order.save()

                messages.info(self.request, "The Purchase has been authorized")
                return redirect("/")
            
            except stripe.error.CardError as e:
                error = e.json_body.get('error' {})
                messages.info(self.request, f"{error.get('message')}")
                return redirect("/")
            
            except stripe.error.InvalidRequestError as e:
                print(e)
                messages.info(self.request, "The given parameters are invalid")
                return redirect("/")
            
            except stripe.error.AuthenticationError as e:
                messages.info(self.request, "Not Authenticated")
                return redirect("/")
            
            except stripe.error.StripeError as e:
                messages.info(self.request, "Something went wrong. Please Try Again")
                return redirect("/")
        
        messages.info(self.request, "Invalid data submitted")
        return redirect("/payment/stripe/")

    
class HomeDesign(ListView):
    template_name = "home.html"
    model = Item

class ViewOrder(View, LoginRequiredMixin):
    def obtainOrder(self, *args, **kwargs):
        try:
            context = { 'object': Order.objects.get(user=self.request.user, ordered=False)}
            
            return render(self.request, 'order_summary.html', context)
            
        except ObjectDoesNotExist:
            messages.warning(self.request, "This order does not exist")
            return redirect("/")


class ItemSummary(DetailView):
    model = Item
    template_name = "product.html"


@login_required
def insert_item(slug, request):
    ordered_item, created_item = OrderItem.objects.get_or_create(item=get_object_or_404(Item, slug=slug), user=request.user, ordered=False)
    current_order = Order.objects.filter(user=request.user, ordered=False)
    if current_order.exists():
        order = current_order[0]
        filtered = ordered_item.items.filter(item_slug=ordered_item.slug)
        if filtered.exists():
            num_of_items = num_of_items + 1
            ordered_item.save()
            messages.info(request, "We've just added one more item")
            return redirect("core:order-summary")
        else:
            order.items.add(ordered_item)
            messages.info(request, "This item has been added to your shopping cart")
            return redirect("core:order-summary")
    else:
        date = timezone.now()
        order = Order.objects.create(
            user=request.user, date = date
        )
        current_order.items.add(ordered_item)
        messages.info(request, "This item was added to your cart")
        return redirect("core:order-summary")

@login_required
def remove_item(slug, request):
    ordered_item = Order.objects.filter(user=requst.user, ordered=False)
    if ordered_item.exists():
        order = ordered_item[0]
        if order.items.filter(item_slug=ordered_item.slug).exists():
            item_order = OrderItem.objects.filter(item=item, user=request.user, ordered=False)
            item_order = item_order[0]
            order.items.remove(item_order)
            messages.info(request, "This item was removed from your shopping cart")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item is not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.infor(request, "This item doesn't exist")
        return redirect("core:product", slug=slug)


def obtain_coupon(code, request):
    try:
         return UseCoupon(self.request.POST or None)
    except ObjectDoesNotExist:
        messages.info(request, "This item does not exist")
        return redirect("core:checkout")


class ApplyCoupon:
    def post(self, *args, **kwargs):
        newForm = UseCoupon(self.request.POST or None)
        if newForm.is_valid():
            try:
                found_code = OrderItem.objects.get('code')
                order_results = OrderItem.objects.get(user=user.request.user, ordered=False)
                order_results.coupon = obtain_coupon(found_code, self.request)
                order_results.save()
                messages.info(self.request, "Added Coupon to your account")
                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "Order does not exist")
                return redirect("core:checkout")


class RequestNewRefund:
    def get(self, *args, **kwargs):
        return render(self.request, "request_refund.html", {'form': refundForm()})
    
    def post(self, *args, **kwargs):
        completed_form = refundForm(self.request.POST)
        if completed_form.is_valid():
            code = completed_form.cleaned_data.get('code')
            msg = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')

            try:
                order = OrderItem.objects.get(code=code)
                order.refund_submitted = True
                order.save()

                obtained_refund = Refund()
                refund.order = order
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request has been submitted")
                return redirect("core:request-refund")
            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist")
                return redirect("core:request-refund")
