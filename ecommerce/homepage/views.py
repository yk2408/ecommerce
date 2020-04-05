from django.shortcuts import render
from categoryandproduct.models import ElectronicProduct


def homepage(request):
    product = ElectronicProduct.objects.all()
    x = [int(((i.price - i.special_price) / i.price) * 100) for i in product]
    context = {
                'product': product,
                'discount': x,
              }

    return render(request, 'index.html', context)


def about_us(request):
    context = {}
    return render(request, 'about-us.html', context)
