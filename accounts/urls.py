from django.urls import path
from accounts.views import login_page, register_page, logout_page, activate_email, cart, add_to_cart, remove_cart_item, remove_coupon, success

urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout/', logout_page, name='logout'),
    path('activate/<email_token>/', activate_email, name='activate_email'),
    path('cart/', cart, name='cart'),
    path('add-to-cart/<uid>/', add_to_cart, name= 'add_to_cart'),
    path('remove-cart-item/<uid>/', remove_cart_item, name= 'remove_cart_item'),
    path('remove-coupon/<uid>/', remove_coupon, name= 'remove_coupon'),
    path('success/', success, name='success')
]
