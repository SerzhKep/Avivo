# Generated by Django 4.0.4 on 2022-05-18 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_rename_date_pod_product_date_pob'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='date_pob',
            new_name='date_pub',
        ),
    ]
