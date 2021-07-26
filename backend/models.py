from backend.input import OrderItem
from django.db import models
from django.conf import settings
from django.db.models import Sum;
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.db.models.signals import post_save
import enum
import math

class Status(enum.Enum):
    Nonexistent = 0
    Pending = 1
    Active = 2


MAILING_MODES = (
    ('S', 'Shipping'),
    ('B', 'Billing')
)



class AccountProfile(models.Model):
    my_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pay_with_click = models.BooleanField(default=False)
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)

    def _str_(self):
       return self.my_user


class Item(models.Model):
    name_of_item = models.CharField(max_length=1000)
    price_of_item = models.FloatField()
    number_of_given_item = models.IntegerField(default = 1)
    discount = models.FloatField(choices=CATEGORY_CHOICES, max_length=3)

    slug = models.SlugField()
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    text_about_item = models.TextField()
    image = models.ImageField()

    def _str_(self):
        return self.name_of_item

    def add_to_cart(self):
        addr = "backend:add-to-cart"
        rev_args = {'slug': self.slug}
        return reverse(addr, rev_args)

    def remove_from_cart(self):
        addr = "backend:remove-from-cart"
        rev_args = {'slug': self.slug}
        return reverse(addr, rev_args)
    
    def get_link(self):
        rev_args = {'slug': self.slug}
        return reverse("core:product", rev_args)
    



class BuyItem(models.Model):
    my_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_item = models.BooleanField(default=False)
    given_item = models.ForeignKey(Item, on_delete=models.CASCADE)
    number_of_given_item = models.IntegerField(default=1)

    def get_agg_price(self):
        return self.number_of_given_item * self.given_item.price

    def get_agg_price_with_discount(self):
        return self.number_of_given_item * self.discount

    def get_official_price(self):
        total_price = 0
        if self.item.discount:
            total_price = self.get_agg_price_with_discount()
        total_price = self.get_agg_price()
        return total_price

    def _str_(self):
        return f"{self.number_of_given_item} of {self.item.name_of_item}"
    

class MakeOrder(models.Model):
    items = models.ManyToManyField(BuyItem)
    user_account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item_code = models.CharField(max_lengtH=1000, blank=True, null=True)

    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    shipping_date = models.DateTimeField(BuyItem)
    order_date = models.DateTimeField()

    shipping_address = models.ForeignKey('Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey('Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)

    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)

    currently_delivered = False
    recieved = False
    recieved_refund = False
    refunded = False
    order_status = Status.Nonexistent


    def _str_(self):
        return self.user_account.username
    
    def item_received(self, input):
        if input and order_status != Status.Nonexistent:
            recieved = True
        return recieved
    
    def item_refunded(self, input):
        if input and order_status != Status.Nonexistent:
            order_status = 0
            refunded = True
        return refunded
    
    def calculate_total_price(self):
        if order_status != Status.Nonexistent:
            return math.nan
        items = self.items.all()
        for item in items:
            total = total + item.get_official_price()
        if self.coupon:
            total = total - self.coupon.amount
        return total
    
    def get_status(self):
        return self.order_status


class Address(models.Model):
    str_address = models.CharField(max_length=1000)
    user_account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    country = CountryField(multiple=False)
    zip_code = models.CharField(max_length=1000)

    def _str_(self):
        return self.user_account.username
    

class Coupon(models.Model):
    value = models.CharField(max_length=100)
    amt_of_coupons = models.FloatField()

    def _str_(self):
        return self.code


class UserGroup(models.Model):
    account_name = models.CharField(max_length=100)
    num_of_followers = models.IntegerField(default=10)
    
    def _str_(self):
        return self.account_name
    


class FriendGroup(models.Model):
    friend_name = models.CharField(max_length=100)
    link_to_account = models.URLField(max_length=200)
    key = models.ForeignKey(UserGroup)



class Payment(models.Model):
    stripe_key = models.CharField(max_length=300)
    user_act = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

    value = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.user_act.username


class Refund(models.Model):
    order = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def _str_(self):
        return f"{self.pk}"

class createAcct(AccountProfile):
    def send(inst, created):
        if created:
            userprofile = AccountProfile.objects.create(user=inst)



post_save.connect(sendReq.send, sender=settings.AUTH_USER_MODEL)
    





