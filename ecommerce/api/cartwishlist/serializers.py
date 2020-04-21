from django.contrib.auth.models import User
from rest_framework import serializers
import json
from cart.models import CartItem, WishList
from categoryandproduct.models import ElectronicProduct


class CartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(
        write_only=True, error_messages={
            'required': "Product id is required",
            'invalid': "Please enter valid product id",
            'blank': "Product id should not be blank",
    })
    quantity = serializers.IntegerField(error_messages={
        'required': "quantity is required",
        'invalid': "Please enter valid quantity",
        'blank': "quantity should not be blank",
    })

    def to_representation(self, instance):
        data = {
                'id': instance.id,
                'product_id': instance.product.id,
                'product_image': json.dumps(str(instance.product.product_image)),
                'unit_price': instance.product.special_price,
                'quantity': instance.quantity,
                'total': instance.price,
                'created_at': instance.created_at
                }
        print("DAta--->", data)
        return data

    def create(self, validated_data):
        username = self.context.get("username")
        product_id = validated_data['product_id']
        quantity = validated_data['quantity']
        user = User.objects.get(username=username)
        try:
            product = ElectronicProduct.objects.get(pk=product_id)
        except Exception as e:
            raise serializers.ValidationError(e)
        existing_cart_item = CartItem.objects.filter(user=user, product=product).first()
        # before creating a new cart item check if it is in the cart already
        # and if yes increase the quantity of that item
        if existing_cart_item:
            existing_cart_item.quantity += quantity
            existing_cart_item.price = product.special_price * existing_cart_item.quantity
            existing_cart_item.save()
            return existing_cart_item

        else:
            new_cart_item = CartItem()
            new_cart_item.user = user
            new_cart_item.product = product
            new_cart_item.quantity = quantity
            new_cart_item.price = product.special_price * quantity
            new_cart_item.save()
            return new_cart_item

    def update(self, instance, validated_data):
        product_id = validated_data['product_id']
        quantity = validated_data['quantity']
        try:
            product = ElectronicProduct.objects.get(pk=product_id)
        except Exception as e:
            raise serializers.ValidationError(e)
        instance.product = product
        instance.quantity = quantity
        instance.price = product.special_price * quantity
        instance.save()
        return instance


class WishListSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(
        write_only=True, error_messages={
            'required': "Product id is required",
            'invalid': "Please enter valid product id",
            'blank': "Product id should not be blank",
    })

    def to_representation(self, instance):
        data = {
                'id': instance.id,
                'product_id': instance.product.id,
                'product_image': json.dumps(str(instance.product.product_image)),
                'product_name': instance.product.name,
                'unit_price': instance.product.special_price
                }
        return data

    def create(self, validated_data):
        username = self.context.get("username")
        product_id = validated_data['product_id']
        user = User.objects.get(username=username)
        try:
            product = ElectronicProduct.objects.get(pk=product_id)
        except Exception as e:
            raise serializers.ValidationError(e)
        existing_wishlist_item = WishList.objects.filter(user=user, product=product).first()
        if existing_wishlist_item:
            raise serializers.ValidationError('Item already added in Wish list')

        else:
            new_wishlist_item = WishList(user=user, product=product)
            new_wishlist_item.save()
            return new_wishlist_item





