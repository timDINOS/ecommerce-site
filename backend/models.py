from django.db import models
from django.conf import settings
from django.db.models import Sum;


class AccountProfile(models.Model):
    def _str_(self):
       return
     
class Payment(models.Model):
    pass;


class Item(models.Model):
    name_of_item = models.CharField(max_length=1000)

    def _str_(self):
        return self.name_of_item


class Coupon(models.Model):
    pass;


