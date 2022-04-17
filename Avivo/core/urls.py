# from django.conf.urls import url
from django.urls import path
from .views import index, product


urlpatterns = [
    path('', index, name='index'),
    path('product/', product, name='product'),
]