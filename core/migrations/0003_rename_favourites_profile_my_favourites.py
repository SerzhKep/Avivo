# Generated by Django 4.0.4 on 2022-05-02 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_profile_favourites'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='favourites',
            new_name='my_favourites',
        ),
    ]