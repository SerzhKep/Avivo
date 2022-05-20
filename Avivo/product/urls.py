from django.urls import path
from django.views.generic import TemplateView
from .views import (IndexView, FeedView, ProductDetail, ProductCreate,
                    product_edit, ProductDelet, product_like
                    )


app_name = 'products'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('products/<int:product_id>/', ProductDetail.as_view(), name='product-detail'),
    path('products/<int:product_id>/edit/', product_edit, name='product-edit'),
    path('products/<int:product_id>/delete/', ProductDelet.as_view(), name='product-delete'),
    path('products/<int:product_id>/like/', product_like, name='product-like'),
    path('products/create/', ProductCreate.as_view(), name='product-create'),
    path('products/success/', TemplateView.as_view(), name='product-delete_success'),
]