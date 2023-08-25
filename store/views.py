from django.shortcuts import render
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)


class ListProducts(ListView):
    template_name = 'store/index_products.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 5

class ProductDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Product
    # Используем другой шаблон — product.html
    template_name = 'store/product.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'product'
