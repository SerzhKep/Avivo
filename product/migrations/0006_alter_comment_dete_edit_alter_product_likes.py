# Generated by Django 4.0.4 on 2022-05-18 10:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0005_remove_product_favourites_product_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='dete_edit',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='like_product', to=settings.AUTH_USER_MODEL),
        ),
    ]
