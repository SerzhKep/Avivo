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
    subscriptions = models.ManyToManyField(User, blank=True, related_name='subscribers')


    def __str__(self):
        return f'Profile of {self.user.username}'

    def get_subscribers_count(self):
        """"Количество подписавшихся пользователей"""
        subscribers_count = self.user.subscribers.count()
        return subscribers_count
        

    def get_subscriptions_count(self):
        """"Количество пользователей на которых пользователь подписался"""
        subscriptions_count = self.subscriptions.count()
        return subscriptions_count


