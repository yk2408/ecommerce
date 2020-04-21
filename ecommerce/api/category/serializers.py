from rest_framework import serializers

from categoryandproduct.models import Category, SubCategory, SubCategoryMenu, Brand


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(error_messages={
        'required': "Category name is required",
        'invalid': "Please enter valid Category name",
        'blank': "Category name should not be blank",
    })

    class Meta:
        model = Category
        fields = ['id', 'name']

    def validate(self, data):
        name = data['name']
        try:
            category = Category.objects.get(name=name)
            raise serializers.ValidationError('Category already exist')
        except Category.DoesNotExist:
            category = None
        return data

    def create(self, validated_data):
        name = validated_data.get("name").title()
        category = Category.objects.create(name=name)
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class SubCategorySerializer(serializers.Serializer):
    name = serializers.CharField(error_messages={
        'required': "SubCategory name is required",
        'invalid': "Please enter valid SubCategory name",
        'blank': "SubCategory name should not be blank",
    })
    category_name = serializers.CharField(error_messages={
        'required': "Category name is required",
        'invalid': "Please enter valid Category name",
        'blank': "Category name should not be blank",
    })

    def create(self, validated_data):
        category_name = validated_data.get("category_name").title()
        name = validated_data.get("name").title()
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            raise serializers.ValidationError('Category not found')
        subcategory = SubCategory.objects.create(name=name, category=category)
        return validated_data

    def update(self, instance, validated_data):
        category_name = validated_data.get("category_name").title()
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            raise serializers.ValidationError('Category not found')
        instance.name = validated_data.get('name', instance.name)
        instance.category = category
        instance.save()
        return validated_data


class SubCategoryMenuSerializer(serializers.Serializer):
    name = serializers.CharField(error_messages={
        'required': "SubCategoryMenu name is required",
        'invalid': "Please enter valid SubCategoryMenu name",
        'blank': "SubCategoryMenu name should not be blank",
    })
    subcategory_name = serializers.CharField(error_messages={
        'required': "SubCategory name is required",
        'invalid': "Please enter valid SubCategory name",
        'blank': "SubCategory name should not be blank",
    })
    category_name = serializers.CharField(error_messages={
        'required': "Category name is required",
        'invalid': "Please enter valid Category name",
        'blank': "Category name should not be blank",
    })

    def create(self, validated_data):
        category_name = validated_data.get("category_name").title()
        subcategory_name = validated_data.get("subcategory_name").title()
        name = validated_data.get("name").title()
        try:
            subcategory = SubCategory.objects.get(name=subcategory_name, category__name=category_name)
        except SubCategory.DoesNotExist:
            raise serializers.ValidationError('SubCategory not found')
        subcategory_menu = SubCategoryMenu.objects.create(name=name, sub_category=subcategory)
        return validated_data

    def update(self, instance, validated_data):
        category_name = validated_data.get("category_name").title()
        subcategory_name = validated_data.get("subcategory_name").title()
        try:
            subcategory = SubCategory.objects.get(name=subcategory_name, category__name=category_name)
        except SubCategory.DoesNotExist:
            raise serializers.ValidationError('SubCategory not found')
        instance.name = validated_data.get('name', instance.name).title()
        instance.sub_category = subcategory
        instance.save()
        return validated_data


class BrandSerializer(serializers.Serializer):
    name = serializers.CharField(error_messages={
        'required': "Brand name is required",
        'invalid': "Please enter valid Brand name",
        'blank': "Brand name should not be blank",
    })
    subcategory_name = serializers.CharField(error_messages={
        'required': "SubCategory name is required",
        'invalid': "Please enter valid SubCategory name",
        'blank': "SubCategory name should not be blank",
    })
    category_name = serializers.CharField(error_messages={
        'required': "Category name is required",
        'invalid': "Please enter valid Category name",
        'blank': "Category name should not be blank",
    })

    def create(self, validated_data):
        category_name = validated_data.get("category_name").title()
        subcategory_name = validated_data.get("subcategory_name").title()
        name = validated_data.get("name").title()
        try:
            subcategory = SubCategory.objects.get(name=subcategory_name, category__name=category_name)
        except SubCategory.DoesNotExist:
            raise serializers.ValidationError('SubCategory not found')
        brand = Brand.objects.create(name=name, sub_category=subcategory)
        return validated_data

    def update(self, instance, validated_data):
        category_name = validated_data.get("category_name").title()
        subcategory_name = validated_data.get("subcategory_name").title()
        try:
            subcategory = SubCategory.objects.get(name=subcategory_name, category__name=category_name)
        except SubCategory.DoesNotExist:
            raise serializers.ValidationError('SubCategory not found')
        instance.name = validated_data.get('name', instance.name).title()
        instance.sub_category = subcategory
        instance.save()
        return validated_data
