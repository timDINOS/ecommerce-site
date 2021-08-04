from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.conf import settings
from backend.models import AccountProfile
from autoslug import AutoSlugField


class MyProfile(models.Model):
    AccountProfile()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    bio = models.CharField(max_length = 1000, blank=True)
    friends = models.ManyToManyField("Profile", blank=True)
    slug = AutoSlugField(populate_from='user')

    def _str_(self):
        return str(self.user.username)
    
    def get_url(self):
        return "/users/{}".format(self.slug)
    

class FriendRequest(models.Model):
    friend = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="friend", on_delete=models.CASCADE)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return "{} wants to connect with {}".format(self.from_user.username, self.to_user.username)

def post_save_model(sender, created, object, *args, **kwargs):
    if created == True:
        try: 
            MyProfile.objects.create(user=object)
        except:
            pass

post_save.connect(post_save_model, sender=settings.AUTH_USER_MODEL)
