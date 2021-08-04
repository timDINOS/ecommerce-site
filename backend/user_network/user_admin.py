from django.contrib import admin
from backend.user_network.user_models import MyProfile, FriendRequest

admin.site.register(MyProfile)
admin.site.register(FriendRequest)