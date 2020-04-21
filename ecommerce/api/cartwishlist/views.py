from django.shortcuts import render
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from api.base.views import BaseView, get_response
from api.cartwishlist.serializers import CartSerializer, WishListSerializer
from api.common.authentication import CustomAuthentication
from cart.models import CartItem, WishList


# Cart Api view :-


class CartApi(BaseView):
    authentication_classes = (CustomAuthentication, JSONWebTokenAuthentication)

    def get_object(self, pk, user):
        try:
            return CartItem.objects.get(pk=pk, user=user)
        except CartItem.DoesNotExist:
            raise serializers.ValidationError('Details not found')

    # Add to cart:-
    def post(self, request):
        context = {'username': request.user.username}
        serializer = CartSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = get_response(message='Electronic Product Added successfully', result=serializer.data)
        return Response(response, status=response["status_code"])

    # Update CartItem :-
    def put(self, request, pk):
        user = request.user
        cart_instance = self.get_object(pk, user)
        serializer = CartSerializer(cart_instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = get_response(message='CartItem Updated successfully', result=serializer.data)
        return Response(response, status=response["status_code"])

    # Delete CartItem :-
    def delete(self, request, pk):
        user = request.user
        cart_instance = self.get_object(pk, user)
        cart_instance.delete()
        response = get_response(message='CartItem Deleted successfully', result={})
        return Response(response, status=response["status_code"])

    # CartItems List:-

    def get(self, request, format=None):
        user = request.user
        cart_item_list = [cart.product.name for cart in CartItem.objects.filter(user=user)]
        response = get_response(message='CartItem list fetched successfully', result=cart_item_list)
        return Response(response, status=response["status_code"])

# WishList Api view :-


class WishListApi(BaseView):
    authentication_classes = (CustomAuthentication, JSONWebTokenAuthentication)

    def get_object(self, pk, user):
        try:
            return WishList.objects.get(pk=pk, user=user)
        except WishList.DoesNotExist:
            raise serializers.ValidationError('Details not found')

    # Add to wishlist:-
    def post(self, request):
        context = {'username': request.user.username}
        serializer = WishListSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = get_response(message='Item Added successfully', result=serializer.data)
        return Response(response, status=response["status_code"])

    # Delete CartItem :-
    def delete(self, request, pk):
        user = request.user
        wish_list_instance = self.get_object(pk, user)
        wish_list_instance.delete()
        response = get_response(message='WishList Item Deleted successfully', result={})
        return Response(response, status=response["status_code"])

    # CartItems List:-

    def get(self, request, format=None):
        user = request.user
        print('user----->', user)
        wish_list_items = [wish_list.product.name for wish_list in WishList.objects.filter(user=user)]
        response = get_response(message='CartItem list fetched successfully', result=wish_list_items)
        return Response(response, status=response["status_code"])
