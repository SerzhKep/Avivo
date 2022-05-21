from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.views.generic import (ListView, DetailView, CreateView,
                                  DeleteView, UpdateView)
from django.core.exceptions import PermissionDenied
from .models import Product, Comment
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

    def post(self, request, *args, **kwargs):
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


class ProductCreate(CreateView):
    form_class = ProductForm
    template_name = 'products/create.html'

    @method_decorator(login_required(login_url='/admin/'))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @method_decorator(login_required(login_url='/admin/'))
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            product =form.save(commit=False)
            product.author = request.user
            product.save()
            return redirect(reverse('products:product-detail',
                                    kwargs={'product_id': product.id}))
        else:
            return render(request, 'products/create.html', {'form': form})


class ProductDelet(DeleteView):
    model = Product
    pk_url_kwarg = 'product_id'
    template_name = 'products/delete.html'

    def get_success_url(self):
        return reverse('products:product-delete-success')


class CommentDelet(DeleteView):
    model = Comment
    pk_url_kwarg = 'id'

    def get_success_url(self):
        comment_id = self.kwargs['id']
        comment = Comment.objects.get(id=comment_id)
        return reverse('products:product-detail',
                        args=(comment.product.id, ))


class ProductUpdate(UpdateView):
    form_class = ProductForm
    model = Product
    template_name = 'products/update.html'
    pk_url_kwarg = 'product_id'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.request.user != obj.author:
            raise PermissionDenied('Вы не автор этого продукта!')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        image = self.object.image
        description = self.object.description
        form = self.get_form()

        if form.is_valid():
            if image != form.cleaned_data['image'] or description != form.cleaned_data['description']:
                self.object.likes.clear()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def get_success_url(self):
        product_id = self.kwargs['product_id']
        return reverse('products:product-detail', args=(product_id, ))



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