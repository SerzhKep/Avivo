from django.urls import path
from .views import (index, feed, product_detail, product_create,
                    product_edit, product_delet, favorit_product
                    )


app_name = 'product'

urlpatterns = [
    path('', index, name='index'),
    path('feed/', feed, name='my-feed'),
    path('product/<int:product_id>/', product_detail, name='product-detail'),
    path('product/<int:product_id>/edit/', product_edit, name='product-edit'),
    path('product/<int:product_id>/delet/', product_delet, name='product-delet'),
    path('product/<int:product_id>/favorit/', favorit_product, name='favorit-product'),
    path('product/create/', product_create, name='product-create'),
]