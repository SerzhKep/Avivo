from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User


def user_avatar_path(instance, filename):
    user_id = instance.user.id
    return f'user_{user_id}/avatar/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='profile')
    birte_date = models.DateField(blank=True, null=True)
    about = models.TextField(max_length=1000, blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='subscribers')


    def __str__(self):
        return f'Profile of {self.user.username}'




