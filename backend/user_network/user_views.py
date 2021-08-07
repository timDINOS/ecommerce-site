from backend.user_network.user_models import MyProfile, FriendRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponseRedirect
from backend.user_network.user_forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
import random

User = get_user_model()

def friends_list(request):
    p = request.user.profile
    friends = p.friends.all()
    return render(request, "users/friends_list.html", {'friends': friends})

@login_required
def users_list(request):
    users = MyProfile.objects.exclude(user=request.user)
    send_req = FriendRequest.objects.filter(from_user=request.user)
    my_friends = request.user.profile.friends.all()
    sent_rec = []
    friends = []
    for friend in my_friends:
        friend = user.friends.all()
        for f in friend:
            if f in friends:
                friend += friend.exclude(user=f.user)
        my_friends += friend
        