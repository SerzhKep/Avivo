from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.db.models import Count
from .models import Product


def index(request):
    products = Product.objects.annotate(favorit_nums=Count('favourites')).order_by('-favorit_nums')[:10]
    context = {
        'popular_product': products
    }
    return render(request, 'product/index.html', context)


def feed(request):
    products = Product.objects.filter(author__in=request.user.profile.subscribers.all())
    response = [f'id: {product.id}| autor:{product.author}' for product in products]
    return HttpResponse(response)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product/detail.html', {'product': product})


def product_edit(request, product_id):
    response = f'Изменение продукта #{product_id}'
    return HttpResponse(response)


def product_create(request):
    return HttpResponse('Создание нового продукта!')


def product_delet(request, product_id):
    response = f'Удалили продукт #{product_id}'
    return HttpResponse(response)


def favorit_product(request, product_id):
    response = f'Добавили продукт в избранное #{product_id}'
    return HttpResponse(response)