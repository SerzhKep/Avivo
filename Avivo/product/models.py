from distutils.command.upload import upload
from email.mime import image
from time import strftime
from django.db import models
from django.contrib.auth.models import User


def user_product_image_path(instance, filename):
    user_id = instance.author.id
    return f'user_{user_id}/product/{filename}'


class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_product_image_path)
    description = models.TextField(max_length=1000, blank=True)
    date_pub = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, blank=True, related_name='like_product')


    @property
    def likes_count(self):
        return self.likes.count()

    def get_date_pub(self):
        return strftime("%d.%m.%Y г. %H:%M")

    def __str__(self):
        return f'product {self.id}, author {self.author.username}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=50)
    date_pub = models.DateTimeField(auto_now_add=True)
    dete_edit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'author - {self.author.username}, publicatede - {self.date_pub}, product - {self.product.description[:15]}...'
