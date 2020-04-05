from django.contrib import admin
from .models import Category, SubCategory, Brand, ElectronicProduct, Product, SubCategoryMenu


# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_filter = ['name', ]
    search_fields = ['name', ]


class ElectronicProductAdmin(admin.ModelAdmin):
    list_filter = [
                    'brand',
                    'name',
                    'price'
                    ]
    # list_display = ['name',
    #                 'category_name',
    #                 'price'
    #                 ]
    #
    # def category_name(self, instance):
    #     return instance.category.name


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory)
admin.site.register(Brand)
admin.site.register(ElectronicProduct, ElectronicProductAdmin)
admin.site.register(Product)
admin.site.register(SubCategoryMenu)