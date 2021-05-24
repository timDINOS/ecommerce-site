from django.db import models
from django.conf import settings
from django.db.models import Sum;


class AccountProfile(models.Model):
    my_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pay_with_click = models.BooleanField(default=False)

    def _str_(self):
       return self.my_user


class Item(models.Model):
    name_of_item = models.CharField(max_length=1000)

    def _str_(self):
        return self.name_of_item


class Payment(models.Model):
    my_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_item = models.BooleanField(default=False)
    given_item = models.ForeignKey(Item, on_delete=models.CASCADE)
    number_of_given_item = models.IntegerField(default=1)

    def get_agg_price(self):
        return self.number_of_given_item * self.given_item.price"

    def _str_(self):
        return f"{self.number_of_given_item} of {self.item.name_of_item}"
    



class Coupon(models.Model):
    value = models.CharField(max_length=100)
    amt_of_coupons = models.FloatField()

    def _str_(self):
        return self.code





