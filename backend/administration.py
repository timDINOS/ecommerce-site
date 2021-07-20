from backend.input import OrderItem
from django.contrib import admin

from .models import AccountProfile, BuyItem


class AdminRequests(admin.ModelAdmin):
    request_admin = ['user', 
                     'ordered', 
                     'currently_delivered', 
                     'recieved', 
                     'refund_requested',
                     'refund_request_accepted', 
                     'shipping_address',
                     'billing_address', 
                     'payment',
                     'coupon'
                     ]
    list_display_links = ['user', 'shipping_address', 'billing_address', 'payment', 'coupon']
    list_filter = ['ordered', 'being_delivered', 'recieved', 'refund_requested', 'refund_granted']
    search_fields = ['user_username', 'item_name']
                     

class AdminLocation(admin.ModelAdmin):
    loc_admin = [
        'name',
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'address_type',
        'default'
    ]

    filtered_list = ['default', 'address_type', 'country']
    search_filters = ['name', 'street_address', 'apartment_address', 'zip']



admin.site.register(AccountProfile)
admin.site.register(AdminLocation)
admin.site.register(OrderItem)
admin.site.register(BuyItem)

