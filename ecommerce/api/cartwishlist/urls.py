from django.urls import path, re_path
from .views import CartApi, WishListApi


urlpatterns = [

    # Cart Api Urls:-
    path('cart/add/', CartApi.as_view(), name='cart-add-api'),
    path('cart/update/<int:pk>/', CartApi.as_view(), name='cart-update-api'),
    path('cart/delete/<int:pk>/', CartApi.as_view(), name='cart-delete-api'),
    path('cart/list/', CartApi.as_view(), name='cart-list-api'),

    # WishList Api Urls:-
    path('wish-list/add/', WishListApi.as_view(), name='wish-list-add-api'),
    path('wish-list/delete/<int:pk>/', WishListApi.as_view(), name='wish-list-delete-api'),
    path('wish-list/items/', WishListApi.as_view(), name='wish-list-items-api'),
]
