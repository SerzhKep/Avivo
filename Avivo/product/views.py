import re
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.db.models import Count
from .models import Product
from .forms import ProductForm


def index(request):
    products = Product.objects.annotate(likes_nums=Count('likes')).order_by('-likes_nums')[:10]
    context = {
        'popular_products': products
    }
    return render(request, 'products/index.html', context)


def feed(request):
    products = Product.objects.filter(author__in=request.user.profile.subscribers.all())
    response = [f'id: {product.id}| autor:{product.author}' for product in products]
    return HttpResponse(response)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/detail.html', {'product': product})


def product_edit(request, product_id):
    response = f'Изменение продукта #{product_id}'
    return HttpResponse(response)


def product_create(request):
    form = ProductForm()
    if request.method == 'GET':
        return render(request, 'products/create.html', {'form': form})
    elif request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product =form.save(commit=False)
            product.author = request.user
            product.save()
            return redirect(reverse('products:product-detail', kwargs={'product_id': product.id}))
        else:
            return render(request, 'products/create.html', {'form': form})
    
    return HttpResponse('Создание нового продукта!')


def product_delet(request, product_id):
    response = f'Удалили продукт #{product_id}'
    return HttpResponse(response)


def product_like(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    if user in product.likes.all():
        product.likes.remove(user)
    else:
        product.likes.add(user)
        product.save()
    return redirect(request.META.get('HTTP_REFERER'), request)