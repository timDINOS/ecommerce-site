from django.contrib import admin

from .models import AccountProfile


class AdminRequests(admin.ModelAdmin):


class AdminLocation(admin.ModelAdmin):


admin.site.register(AccountProfile)

