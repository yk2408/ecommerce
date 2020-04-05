from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

from categoryandproduct.models import ElectronicProduct

from order.models import ManageAddress

from order.forms import AddAddressForm
from .forms import CartItemForm, WishListForm
from .models import CartItem, WishList


# Create your views here.


# @login_required(login_url="/userprofile/login")
def add_cart(request, slug):
    if request.is_ajax():
        if not request.user.is_authenticated:
            return JsonResponse({'authenticated': False})
        else:
            print('authenticated------------------------------------>')
            cart_form = CartItemForm()
            username = request.user.username
            user_id = User.objects.get(username=username)
            product_id = ElectronicProduct.objects.get(id=slug)
            try:
                cart_item = CartItem.objects.get(user__username=username, product__name=product_id)
            except CartItem.DoesNotExist:
                cart_item = None
            if cart_item is not None:
                cart_form = CartItemForm(instance=cart_item)
                cart_profile = cart_form.save(commit=False)
                cart_profile.quantity = cart_item.quantity + 1
                cart_profile.save()
                return JsonResponse({"status": "Added"})
            else:
                cart_profile = cart_form.save(commit=False)
                cart_profile.user = user_id
                cart_profile.product = product_id
                cart_profile.price = product_id.special_price
                cart_profile.save()
                return JsonResponse({"status": "Added"})
    return redirect('/')


def my_cart(request):
    username = request.user.username
    if request.method == "POST" and request.is_ajax():
        inc = int(request.POST['inc'])
        name = request.POST['product_name']
        user_id = CartItem.objects.get(user__username=username, product__name=name)
        if inc == 0:
            user_id.delete()
            return JsonResponse({'status': '200'})
        else:
            if user_id:
                cart_form = CartItemForm(instance=user_id)
                quantity = cart_form.instance.quantity + inc
                cart_profile = cart_form.save(commit=False)
                cart_profile.quantity = quantity
                cart_profile.save()

    q_s = CartItem.objects.filter(user__username=username)
    sub_total = 0

    for i in q_s:
        sub_total += i.product.special_price * i.quantity

    delivery_charge = "Free"
    total = sub_total
    if sub_total < 30000:
        delivery_charge = 40
        total = sub_total + delivery_charge

    request.session['sub_total'] = sub_total
    request.session['total'] = total
    request.session['delivery_charge'] = delivery_charge

    context = {
                'qs': q_s,
                'sub_total': sub_total,
                'delivery_charge': delivery_charge,
                'total': total

              }
    return render(request, 'cart.html', context)


def remove_cart(request, slug):
    username = request.user.username
    if request.is_ajax() and request.method == "POST":
        qs = CartItem.objects.get(user__username=username, product__id=slug)
        qs.delete()
        return JsonResponse({'status': '200'})

    return redirect("/cart/mycart/")


@login_required(login_url="/userprofile/login")
def add_wish_list(request, slug):
    if request.is_ajax():
        wish_form = WishListForm()
        username = request.user.username
        user_id = User.objects.get(username=username)
        product_id = ElectronicProduct.objects.get(id=slug)
        print(product_id)
        try:
            wish_item = WishList.objects.get(user__username=username, product__name=product_id)
        except WishList.DoesNotExist:
            wish_item = None
        if wish_item is None:
            wish_profile = wish_form.save(commit=False)
            wish_profile.user = user_id
            wish_profile.product = product_id
            wish_profile.save()
            return JsonResponse({"status": "Added"})
        else:
            return JsonResponse({"status": "Already"})
    return redirect('/')


def my_wish_list(request):
    username = request.user.username
    wish_item = WishList.objects.filter(user__username=username)
    context = {
        'wish_item': wish_item
    }
    return render(request, 'wishlist.html', context)


def remove_wish(request, slug):
    username = request.user.username
    if request.is_ajax() and request.method == "POST":
        qs = WishList.objects.get(user__username=username, product__id=slug)
        qs.delete()
        return JsonResponse({'status': '200'})

    return redirect("/cart/mywishlist/")


def checkout(request):
    username = request.user.username
    add_address_form = AddAddressForm(request.POST or None)
    address_qs = ManageAddress.objects.filter(user__username=username)
    if request.method == "GET" and request.is_ajax():
        address = request.GET['add_id']
        request.session['address_id'] = address
        delivery_id = request.session['address_id']

    context = {'address': address_qs,
               'add_address_form': add_address_form
               }
    return render(request, 'checkout.html', context)
