from rest_framework import serializers

from categoryandproduct.models import ElectronicProduct


# Only For Electronic Product :-

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectronicProduct
        fields = '__all__'

    def create(self, validated_data):
        electronic_product = ElectronicProduct.objects.create(**validated_data)
        return electronic_product

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)



