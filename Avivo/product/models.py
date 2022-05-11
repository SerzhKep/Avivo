from distutils.command.upload import upload
from email.mime import image
from django.db import models
from django.contrib.auth.models import User


def user_product_image_path(instance, filename):
    user_id = instance.author.id
    return f'user_{user_id}/product/{filename}'


class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_product_image_path)
    description = models.TextField(max_length=1000, blank=True)
    date_pod = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes_product')


    @property
    def likes_count(self):
        return self.likse.count()

    def __str__(self):
        return f'product {self.id}, author {self.author.username}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.CharField(max_length=50)
    dete_pub = models.DateTimeField(auto_now_add=True)
    dete_edit = models.DateField(auto_now=True)

    def __str__(self):
        return f'author - {self.author.username}, publicatede - {self.dete_pub}, product - {self.product.description[:15]}...'
