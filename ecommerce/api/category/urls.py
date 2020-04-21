from django.urls import path, re_path
from .views import CategoryApi, CategoryListApi, SubCategoryApi, SubCategoryListApi, SubCategoryMenuApi, SubCategoryMenuListApi,\
    BrandApi, BrandListApi


urlpatterns = [
    # Category Api Urls:-
    path('category/add/', CategoryApi.as_view(), name='category-add-api'),
    path('category/update/<int:pk>/', CategoryApi.as_view(), name='category-update-api'),
    path('category/delete/<int:pk>/', CategoryApi.as_view(), name='category-delete-api'),
    path('category/list/', CategoryListApi.as_view(), name='category-list-api'),

    # SubCategory Api Urls:-
    path('subcategory/add/', SubCategoryApi.as_view(), name='subcategory-add-api'),
    path('subcategory/update/<int:pk>/', SubCategoryApi.as_view(), name='subcategory-update-api'),
    path('subcategory/delete/<int:pk>/', SubCategoryApi.as_view(), name='subcategory-delete-api'),
    path('subcategory/list/', SubCategoryListApi.as_view(), name='subcategory-list-api'),

    # SubCategoryMenu Api Urls:-
    path('subcategory-menu/add/', SubCategoryMenuApi.as_view(), name='subcategory-add-api'),
    path('subcategory-menu/update/<int:pk>/', SubCategoryMenuApi.as_view(), name='subcategory-menu-update-api'),
    path('subcategory-menu/delete/<int:pk>/', SubCategoryMenuApi.as_view(), name='subcategory-menu-delete-api'),
    path('subcategory-menu/list/', SubCategoryMenuListApi.as_view(), name='subcategory-menu-list-api'),

    # Brands Api Urls:-
    path('brand/add/', BrandApi.as_view(), name='subcategory-add-api'),
    path('brand/update/<int:pk>/', BrandApi.as_view(), name='brand-api'),
    path('brand/delete/<int:pk>/', BrandApi.as_view(), name='brand-delete-api'),
    path('brand/list/', BrandListApi.as_view(), name='brand-list-api'),

]