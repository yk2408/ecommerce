from django.shortcuts import render

# Create your views here.
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from api.base.views import BaseView, get_response
from api.category.serializers import CategorySerializer, SubCategorySerializer, SubCategoryMenuSerializer, BrandSerializer
from api.common.authentication import CustomAuthentication
from categoryandproduct.models import Category, SubCategory, SubCategoryMenu, Brand


# Category APi Views :-


class CategoryApi(BaseView):
    permission_classes = (IsAdminUser,)
    authentication_classes = (CustomAuthentication, JSONWebTokenAuthentication)
    serializer_class = CategorySerializer

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise serializers.ValidationError('Details not found')

    # Add Category
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = get_response(message='Category Added successfully', result=serializer.data)
        return Response(response, status=response["status_code"])

    # Update Category :-
    def put(self, request, pk):
        category_instance = self.get_object(pk)
        serializer = CategorySerializer(category_instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = get_response(message='Category Updated successfully', result=serializer.data)
        return Response(response, status=response["status_code"])

    # Delete Category :-
    def delete(self, request, pk):
        category_instance = self.get_object(pk)
        category_instance.delete()
        response = get_response(message='Category Deleted successfully', result={})
        return Response(response, status=response["status_code"])

# Category Api List View :-


class CategoryListApi(BaseView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        """
        Return a list of categories.
        """
        category_list = [category.name for category in Category.objects.all()]
        response = get_response(message='Category list fetched successfully', result=category_list)
        return Response(response, status=response["status_code"])


# SubCategory Api Views :-


class SubCategoryApi(BaseView):
    permission_classes = (IsAdminUser,)
    authentication_classes = (CustomAuthentication, JSONWebTokenAuthentication)
    serializer_class = SubCategorySerializer

    def get_object(self, pk):
        try:
            return SubCategory.objects.get(pk=pk)
        except SubCategory.DoesNotExist:
            raise serializers.ValidationError('Details not found')

    # Add SubCategory
    def post(self, request):
        serializer = SubCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = get_response(message='SubCategory Added successfully', result=serializer.data)
        return Response(response, status=response["status_code"])

    # Update SubCategory :-
    def put(self, request, pk):
        subcategory_instance = self.get_object(pk)
        serializer = SubCategorySerializer(subcategory_instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = get_response(message='SubCategory Updated successfully', result=serializer.data)
        return Response(response, status=response["status_code"])

    # Delete SubCategory :-
    def delete(self, request, pk):
        subcategory_instance = self.get_object(pk)
        subcategory_instance.delete()
        response = get_response(message='SubCategory Deleted successfully', result={})
        return Response(response, status=response["status_code"])

# SubCategory Api List View :-


class SubCategoryListApi(BaseView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        """
        Return a list of Subcategories.
        """
        subcategory_list = [category.name for category in SubCategory.objects.all()]
        response = get_response(message='SubCategory list fetched successfully', result=subcategory_list)
        return Response(response, status=response["status_code"])

# SubCategoryMenu Api Views :-


class SubCategoryMenuApi(BaseView):
    permission_classes = (IsAdminUser,)
    authentication_classes = (CustomAuthentication, JSONWebTokenAuthentication)
    serializer_class = SubCategoryMenuSerializer

    def get_object(self, pk):
        try:
            return SubCategoryMenu.objects.get(pk=pk)
        except SubCategoryMenu.DoesNotExist:
            raise serializers.ValidationError('Details not found')

    # Add SubCategoryMenu
    def post(self, request):
        serializer = SubCategoryMenuSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = get_response(message='SubCategoryMenu Added successfully', result=serializer.data)
        return Response(response, status=response["status_code"])

    # Update SubCategoryMenu :-
    def put(self, request, pk):
        subcategory_menu_instance = self.get_object(pk)
        serializer = SubCategoryMenuSerializer(subcategory_menu_instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = get_response(message='SubCategoryMenu Updated successfully', result=serializer.data)
        return Response(response, status=response["status_code"])

    # Delete SubCategory :-
    def delete(self, request, pk):
        subcategory_menu_instance = self.get_object(pk)
        subcategory_menu_instance.delete()
        response = get_response(message='SubCategoryMenu Deleted successfully', result={})
        return Response(response, status=response["status_code"])

# SubCategoryMenu Api List View :-


class SubCategoryMenuListApi(BaseView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        """
        Return a list of Subcategory menus.
        """
        subcategory_menu_list = [subcategory_menu.name for subcategory_menu in SubCategoryMenu.objects.all()]
        response = get_response(message='SubCategoryMenu list fetched successfully', result=subcategory_menu_list)
        return Response(response, status=response["status_code"])

# Brands Api Views :-


class BrandApi(BaseView):
    permission_classes = (IsAdminUser,)
    authentication_classes = (CustomAuthentication, JSONWebTokenAuthentication)
    serializer_class = BrandSerializer

    def get_object(self, pk):
        try:
            return Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            raise serializers.ValidationError('Details not found')

    # Add Brand
    def post(self, request):
        serializer = BrandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = get_response(message='Brand Added successfully', result=serializer.data)
        return Response(response, status=response["status_code"])

    # Update SubCategory :-
    def put(self, request, pk):
        brand_instance = self.get_object(pk)
        serializer = BrandSerializer(brand_instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = get_response(message='Brand Updated successfully', result=serializer.data)
        return Response(response, status=response["status_code"])

    # Delete SubCategory :-
    def delete(self, request, pk):
        brand_instance = self.get_object(pk)
        brand_instance.delete()
        response = get_response(message='Brand Deleted successfully', result={})
        return Response(response, status=response["status_code"])

# Brand Api List View :-


class BrandListApi(BaseView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        """
        Return a list of Brands.
        """
        brand_list = [brand.name for brand in Brand.objects.all()]
        response = get_response(message='Brand list fetched successfully', result=brand_list)
        return Response(response, status=response["status_code"])
