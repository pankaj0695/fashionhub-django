from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from .models import Profile, Cart, CartItem
from products.models import Product, SizeVariant, Coupon
import razorpay

def login_page(request):
  if request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('password')

    user_obj = User.objects.filter(username = email)

    if not user_obj.exists():
      messages.warning(request, 'Account not found.')
      return HttpResponseRedirect(request.path_info)
    
    if not user_obj[0].profile.is_email_verified:
      messages.warning(request, 'Your account is not verified.')
      return HttpResponseRedirect(request.path_info)
    
    user_obj = authenticate(username=email, password=password)
    if user_obj:
      login(request, user_obj)
      return redirect('/')

    messages.warning(request, 'Invalid credentials')
    return HttpResponseRedirect(request.path_info)

  return render(request, 'accounts/login.html')

def register_page(request):
  if request.method == 'POST':
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    password = request.POST.get('password')

    user_obj = User.objects.filter(username = email)

    if user_obj.exists():
      messages.warning(request, 'Email is already taken.')
      return HttpResponseRedirect(request.path_info)
    
    user_obj = User.objects.create(first_name= first_name, last_name=last_name, email=email, username=email)
    user_obj.set_password(password)
    user_obj.save()

    messages.success(request, 'An email has been sent on your mail')
    return HttpResponseRedirect(request.path_info)

  return render(request, 'accounts/register.html')

def logout_page(request):
  logout(request)
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def activate_email(request, email_token):
  try:
    user = Profile.objects.get(email_token = email_token)
    user.is_email_verified = True
    user.save()
    return redirect('/')
  except Exception as e:
    return HttpResponse("Invalid Email token")
  
def cart(request):
  cart = None
  try:
    cart=Cart.objects.get(is_paid=False, user= request.user)
  except Exception as e:
    print(e)
  if request.method == 'POST':
    coupon = request.POST.get('coupon')
    coupon_obj = Coupon.objects.filter(coupon_code = coupon)
    if not coupon_obj.exists():
      messages.warning(request, 'Invalid Coupon.')
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    if cart.coupon:
      messages.warning(request, 'Coupon already exists.')
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    if coupon_obj[0].is_expired:
      messages.warning(request, 'Coupon expired.')
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    if cart.get_cart_total() < coupon_obj[0].minimum_amount :
      messages.warning(request, f'Amount should be greater than {coupon_obj[0].minimum_amount}')
      return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    cart.coupon = coupon_obj[0]
    cart.save()
    messages.success(request, 'Coupon applied')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
     
  payment = None

  if cart:
    client = razorpay.Client(auth = (settings.RAZOR_PAY_KEY_ID, settings.RAZOR_PAY_KEY_SECRET))
    payment = client.order.create({'amount': cart.get_total()*100, 'currency': 'INR', 'payment_capture':1})

    cart.razor_pay_order_id = payment['id']
    cart.save()
  
  context = {
    'cart': cart,
    'payment': payment,
    'user':request.user
  }
  return render(request, 'accounts/cart.html', context)

def add_to_cart(request, uid):
  variant = request.GET.get('variant')
  product = Product.objects.get(uid = uid)
  user = request.user
  cart, _ = Cart.objects.get_or_create(user = user, is_paid = False)

  cart_item = CartItem.objects.create(cart=cart, product = product)
  if variant:
    size_variant = SizeVariant.objects.get(size = variant)
    cart_item.size_variant = size_variant
    cart_item.save()

  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_cart_item(request,uid):
  try:
    cart_item = CartItem.objects.get(uid = uid)
    cart_item.delete()
  except Exception as e:
    print(e)
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_coupon(request, uid):
  try:
    cart = Cart.objects.get(uid = uid)
    cart.coupon=None
    cart.save()
    messages.success(request, 'Coupon removed.')
  except Exception as e:
    print(e)
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def success(request):
  order_id = request.GET.get('order_id')
  cart = Cart.objects.get(razor_pay_order_id = order_id)
  cart.is_paid = True
  cart.save()
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))