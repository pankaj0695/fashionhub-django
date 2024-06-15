from django.contrib import admin
from .models import *

admin.site.register(Category)

class ProductImageAdmin(admin.StackedInline):
  model = ProductImage

class ProductAdmin(admin.ModelAdmin):
  list_display=['product_name', 'price']
  inlines = [ProductImageAdmin]

class ColorVariantAdmin(admin.StackedInline):
  list_display = ['color', 'price']
  model = ColorVariant

class SizeVariantAdmin(admin.StackedInline):
  list_display = ['size', 'price']
  model = SizeVariant
  
admin.site.register(Product, ProductAdmin)
admin.site.register(ColorVariant)
admin.site.register(SizeVariant)
admin.site.register(Coupon)