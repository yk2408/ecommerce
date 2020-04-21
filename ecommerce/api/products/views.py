from django.shortcuts import render
from rest_framework import serializers
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from api.base.views import BaseView, get_response
from api.common.authentication import CustomAuthentication
from api.products.serializers import ProductSerializer
from categoryandproduct.models import ElectronicProduct

# Product Api View :-


class ProductApi(BaseView):
    permission_classes = (IsAdminUser,)
    authentication_classes = (CustomAuthentication, JSONWebTokenAuthentication)

    def get_object(self, pk):
        try:
            return ElectronicProduct.objects.get(pk=pk)
        except ElectronicProduct.DoesNotExist:
            raise serializers.ValidationError('Details not found')

    # Add Only Electronic Product:-
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = get_response(message='Electronic Product Added successfully', result=serializer.data)
        return Response(response, status=response["status_code"])

    # Update Product :-
    def put(self, request, pk):
        product_instance = self.get_object(pk)
        serializer = ProductSerializer(product_instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = get_response(message='Product Updated successfully', result=serializer.data)
        return Response(response, status=response["status_code"])

    # Delete Product :-
    def delete(self, request, pk):
        product_instance = self.get_object(pk)
        product_instance.delete()
        response = get_response(message='Product Deleted successfully', result={})
        return Response(response, status=response["status_code"])

# Product Details Api :-


class ProductDetailsApi(BaseView):
    permission_classes = (AllowAny, )

    def get_object(self, pk):
        try:
            return ElectronicProduct.objects.get(pk=pk)
        except ElectronicProduct.DoesNotExist:
            raise serializers.ValidationError('Details not found')

    # Get Details:-
    def get(self, request, pk):
        product_instance = self.get_object(pk)
        userprofile_details = ProductSerializer(product_instance)
        response = get_response(message='Product Details Fetched successful', result=userprofile_details.data)
        return Response(response, status=response["status_code"])

# Product List Api:-


class ProductListApi(BaseView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        """
        Return a list of product.
        """
        product_list = [product.name for product in ElectronicProduct.objects.all()]
        response = get_response(message='Product list fetched successfully', result=product_list)
        return Response(response, status=response["status_code"])
