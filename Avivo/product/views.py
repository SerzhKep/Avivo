from tokenize import Comment
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Product
from .forms import ProductForm, CommentForm


class IndexView(ListView):
    model = Product
    template_name = 'products/index.html'
    context_object_name = 'products'
    LIMIT = 10

    def get_queryset(self):
        queryset = self.model.objects.annotate(
            likes_nums=Count('likes')
        ).order_by('-likes_nums')[:self.LIMIT]
        return queryset


class FeedView(IndexView):

    @method_decorator(login_required(login_url='/admin/'))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        friends_list = self.request.user.profile.subscribers.all()
        queryset = Product.objects.filter(author__in=friends_list)
        return queryset


class ProductDetail(DetailView):
    model = Product
    template_name = 'products/detail.html'
    pk_url_kwarg = 'product_id'
    comment_form = CommentForm
    comment_model = Comment


    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=object)
        context['comments'] = self.get_comments()

        if request.user.is_authenticated:
            context['comment_form'] = self.comment_form
        return self.render_to_response(context)

    def product(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.comment_form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.product = self.object
            comment.save()
            form = self.comment_form

        return render(request, self.template_name, context={
            'product': self.object,
            'comments': self.get_comments(),
            'comment_form': form
        })

    def get_comments(self):
        product = self.object
        comments = product.comments.all().order_by('-date_pub')
        return comments



def product_edit(request, product_id):
    response = f'Изменение продукта #{product_id}'
    return HttpResponse(response)

@login_required(login_url='/admin/')
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
            return redirect(reverse('products:product-detail',
                                    kwargs={'product_id': product.id}))
        else:
            return render(request, 'products/create.html', {'form': form})
    
    return HttpResponse('Создание нового продукта!')


def product_delet(request, product_id):
    response = f'Удалили продукт #{product_id}'
    return HttpResponse(response)

@login_required(login_url='/admin/')
def product_like(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    if user in product.likes.all():
        product.likes.remove(user)
    else:
        product.likes.add(user)
        product.save()
    return redirect(request.META.get('HTTP_REFERER'), request)