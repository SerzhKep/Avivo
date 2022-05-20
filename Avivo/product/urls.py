from django.urls import path
from .views import (IndexView, FeedView, ProductDetail, product_create,
                    product_edit, product_delet, product_like
                    )


app_name = 'products'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('products/<int:product_id>/', ProductDetail.as_view(), name='product-detail'),
    path('products/<int:product_id>/edit/', product_edit, name='product-edit'),
    path('products/<int:product_id>/delet/', product_delet, name='product-delet'),
    path('products/<int:product_id>/like/', product_like, name='product-like'),
    path('products/create/', product_create, name='product-create'),
]