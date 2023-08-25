from django.urls import path
from .views import *
urlpatterns = [
   path('products/', ListProducts.as_view(), name='list_products'),
   path('products/<int:pk>', ProductDetail.as_view(), name='product_detail'),

]