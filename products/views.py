from django.shortcuts import render
from products.models import Product

def product(request, slug):
  try:
    product = Product.objects.get(slug = slug)
    context = {
      'product':product,
      'user':request.user
    }

    if request.GET.get('size'):
      size = request.GET.get('size')
      price = product.get_price_by_size(size)
      context['selected_size'] = size
      context['updated_price'] = price

    return render(request, 'product/product.html', context)
  
  except Exception as e:
    print(e)