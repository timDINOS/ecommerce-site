from django.db import models
from django.conf import settings
from django.db.models import Sum;
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.db.models.signals import post_save


MAILING_MODES = (
    ('S', 'Shipping'),
    ('B', 'Billing')
)



class AccountProfile(models.Model):
    my_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pay_with_click = models.BooleanField(default=False)

    def _str_(self):
       return self.my_user


class Item(models.Model):
    name_of_item = models.CharField(max_length=1000)
    price_of_item = models.FloatField()
    number_of_given_item = models.IntegerField(default = 1)
    discount = models.FloatField(choices=CATEGORY_CHOICES, max_length=3)

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
    pass


class FriendGroup(models.Model):
    friend_name = models.CharField(max_length=100)
    link_to_account = models.URLField(max_length=200)
    key = models.ForeignKey(UserGroup)



class Payment(models.Model):
    stripe_key = models.CharField(max_length=300)
    user_act = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

    value = models.FloatField()

    def _str_(self):
        return self.user_act.username



class sendReq(AccountProfile):
    def send(inst, created):
        if created:
            userprofile = AccountProfile.objects.create(user=inst)



post_save.connect(sendReq.send, sender=settings.AUTH_USER_MODEL)
    





