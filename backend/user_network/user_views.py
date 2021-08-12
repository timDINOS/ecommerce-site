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
    for i in my_friends:
        if i in friends:
            friends.remove(i)
    if request.user.profile in friends:
        friends.remove(request.user.profile)
    new_list = random.sample(list(users), min(len(list(users)), 10))
    for n in new_list:
        if n in friends:
            new_list.remove(n)
    for sent in send_req:
        sent_rec.append(sent.to_user)
    return render(request, {'users': friends, 'sent': sent_rec})

def get_friends_list(request):
    return render(request, {'friends': request.user.profile.friends.all()})

