from django.shortcuts import render
from products.models import Product, ProductImage

def product(request, slug):
  try:
    product = Product.objects.get(slug = slug)
    product_images = ProductImage.objects.filter(product_id = product.uid)
    print(product_images[0].image)
    context = {
      'product':product,
      'selected_size': '',
      'selected_img': product_images[0],
      'updated_price': None
    }

    if request.GET.get('size'):
      size = request.GET.get('size')
      price = product.get_price_by_size(size)
      context['selected_size'] = size
      context['updated_price'] = price

    if request.GET.get('img'):
      img = request.GET.get('img')
      context['selected_img'] = ProductImage.objects.get(uid=img)

    return render(request, 'product/product.html', context)
  
  except Exception as e:
    print(e)