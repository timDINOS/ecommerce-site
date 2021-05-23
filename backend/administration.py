from django.contrib import admin

from .models import AccountProfile


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


