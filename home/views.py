from django.shortcuts import render
from products.models import Product

def index(request):
  products = Product.objects.all()
  if request.method == "POST":
    search = request.POST.get('search')
    products = Product.objects.filter(product_name__icontains = search)
  context = {'products': products, 'user':request.user}
  return render(request,'home/index.html', context)
