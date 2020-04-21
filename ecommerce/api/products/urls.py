from django.urls import path, re_path
from .views import ProductApi, ProductDetailsApi, ProductListApi


urlpatterns = [

    # Product Api Urls:-

    path('product/add/', ProductApi.as_view(), name='product-add-api'),
    path('product/update/<int:pk>/', ProductApi.as_view(), name='product-update-api'),
    path('product/delete/<int:pk>/', ProductApi.as_view(), name='product-delete-api'),
    path('product/details/<int:pk>/', ProductDetailsApi.as_view(), name='product-details-api'),
    path('product/list/', ProductListApi.as_view(), name='product-list-api'),
]
