from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
from django.db import models


# when you come back to upgrade, consider to optimize Profile models (followers/ following)
# and Contact, to combine them
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', default='default_profile.png')
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followers', blank=True)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings', blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

    def get_absolute_url(self):
        return reverse('account:user_profile', args=[self.user.username])




