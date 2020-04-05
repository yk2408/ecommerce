
from django.urls import path
from . import views

urlpatterns = [
                path('addtocart/<str:slug>/', views.add_cart, name='addcart'),
                path('mycart/', views.my_cart, name='mycart'),
                path('remove-cart/<str:slug>/', views.remove_cart, name='remove-cart'),
                path('remove-wish/<str:slug>/', views.remove_wish, name='remove-wish'),
                path('addtowishlist/<str:slug>/', views.add_wish_list, name='addwish'),
                path('mywishlist/', views.my_wish_list, name='mywishlist'),
                path('checkout/', views.checkout, name='checkout'),
              ]


