from backend.user_network.user_models import MyProfile, FriendRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login
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

@login_required
def send_friend_req(request, id):
    user = get_object_or_404(User, id=id)
    freq = FriendRequest.objects.get_or_create(from_user=request.user, to_user = user)
    return HttpResponseRedirect('/users/{}'.format(user.profile.slug))

@login_required
def reject_req(request, id):
    user = get_object_or_404(User, id=id)
    freq = FriendRequest.objects.filter(from_user = request.user, to_user=user)
    freq = freq.first()
    freq.delete()
    return HttpResponseRedirect('/users/{}'.format(user.profile.slug))


@login_required
def accept_req(request, id):
    from_user = get_object_or_404(User, id=id)
    freq = FriendRequest.objects.filter(from_user = request.user, to_user=user)
    freq = freq.first()
    freq.to_user.profile.friends.add(from_user.profile)
    from_user.profile.friends.add(freq.profile)

@login_required
def search_users(request):
    obj_search_list = User.objects.filter(username_icontins=request.GET.get('q'))
    return render(request, "users/search_users.html", {"users": obj_search_list})


def views(request, response):
    sent_reqs = FriendRequest.objects.filter(from_user = p.user)
    received_reqs =  FriendRequest.objects.filter(to_user = p.user)
    posts = Post.objects.filter(user_name = p.user)

    if MyProfile.objects.filter(slug=slug).first():
        b_status = 'not clicked'

        var length = len(FriendRequest.objects.filter(from_user=request.user).filter(to_user=p.user))
        if (length == 1):
            button_status = 'sent'
        length = len(FriendRequest.objects.filter(from_user=request.user).filter(to_user=request.user))
        if (length == 1):
            button_status = 'received'
        
    return render(request, "users/profile.html", {'me': me, 'button_Status': button_status, 'friends_list': list, 'send_requests': sent_reqs, 'received_requests': received_reqs, 'num_of_posts': posts.count})

    @login_required
    def profile_change(request):
        if request.method != 'POST':
           return render(request, 'users/profile_change.html', {'user': UserUpdateForm(instance=request.user), 'profile': ProfileUpdateForm(instance=request.user),})
        else:
            if (UserUpdateForm(request.POST, instance=request.user).is_valid() and ProfileUpdateForm(request.POST and request.FILES, instance=request.user).is_valid()):
                UserUpdateForm(request.POST, instance=request.user).save()
                ProfileUpdateForm(request.POST, request.FILES, instance=request.user).save()
                return render('my_profile')
    

    def register_me(request):
        if request.method == 'POST' and UserRegisterForm(request.POST).is_valid():
            UserRegisterForm(request.POST).save()
            return render('login_page')
        if request.method != 'POST' and UserRegisterForm(request.POST).is_valid():
            return render(request, 'users/register.html', {'register': UserRegisterForm(request.POST)})
        else:
            return render(request, 'users/register.html', {'register': UserRegisterForm()})
    
    


