from django.urls import path
from .views import *

urlpatterns = [
    
    path('', index, name='index'),
    path('shop/', shop, name='shop'),
    path('search/', search, name='search'),
    path('detail/<int:id>/', detail, name='detail'),
    path('contact/', contact, name='contact'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('cart/', cart, name='cart'),
    path('category/<int:id>', category, name='category'),
    path('addtocart/<int:id>', addtocart, name='addtocart'),
    path('wishlist/', wishlist, name='wishlist'),
    path('checkout/', checkout, name='checkout'),
    path('addtowishlist/<int:id>', addtowishlist, name='addtowishlist'),
    path('deletewishlist/<int:id>', deletewishlist, name='deletewishlist'),
    path('deletecart/<int:id>', deletecart, name='deletecart'),
    path('minus/<int:id>', minus, name='minus'),
    path('plus/<int:id>', plus, name='plus'),
    path('checkout/', checkout, name='checkout'),
    path('confirmorder/<int:id>', confirmorder, name='confirmorder'),
]