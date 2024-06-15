from django.urls import path
from products.views import product

urlpatterns = [
    path('<slug>/', product, name='product')
]
