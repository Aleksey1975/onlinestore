from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Product
from datetime import datetime
from .filters import ProductFilter
from .forms import ProductForm



class ProductsList(ListView):
    model = Product
    ordering = 'name'
    template_name = 'simpleapp/products.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        context['next_sale'] = "Распродажа в среду!"
        context['filterset'] = self.filterset
        return context




class ProductDetail(DetailView):
    model = Product
    template_name = 'simpleapp/product.html'
    context_object_name = 'product'



class ProductCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = ProductForm
    model = Product
    template_name = 'simpleapp/product_edit.html'


class ProductUpdate(LoginRequiredMixin, UpdateView):
    raise_exception = True
    form_class = ProductForm
    model = Product
    template_name = 'simpleapp/product_edit.html'

class ProductDelete(LoginRequiredMixin, DeleteView):
    raise_exception = True
    model = Product
    template_name = 'simpleapp/product_delete.html'
    success_url = reverse_lazy('products_list')