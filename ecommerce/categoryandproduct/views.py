from django.db.models import Q
from django.shortcuts import render
from categoryandproduct.models import ElectronicProduct, SubCategory


def product_details(request, slug):
    product = ElectronicProduct.objects.get(id=slug)
    sort_desc = product.sort_description.split("\r")
    full_desc = product.full_description.split(";")
    heading, details = [], []
    length = range(len(full_desc))
    for i in length:
        if i % 2 == 0:
            heading.append(full_desc[i])
        else:
            details.append(full_desc[i])
    off = int(((product.price - product.special_price) / product.price) * 100)
    context = {'objects': product,
               'off': off,
               'sort_descriptions': sort_desc,
               'full_descriptions': full_desc,
               'heading': heading,
               'details': details,
               }
    return render(request, 'single-product.html', context)


def product_list(request, slug):
    qs = ElectronicProduct.objects.filter(brand__id=slug)
    context = {
               'brand_product': qs,
              }

    return render(request, 'product-list.html', context)


def search_list(request):
    search_value = request.GET.get('q')
    if search_value:
        qs = ElectronicProduct.objects.filter(Q(brand__name__icontains=search_value) | Q(name__icontains=search_value) |
                                              Q(categories=search_value))
        x = [int(((i.price - i.special_price) / i.price) * 100) for i in qs]
        context = {
            'search_product': qs,
            'off': x
        }
    else:
        context = {}
    return render(request, 'search-item.html', context)


