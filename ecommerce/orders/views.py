import stripe
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from cart.models import CartItem
from .models import AddressManage, OrderItem, OrdersDetail, PaymentDetails, CouponCode

# Create your views here.


stripe.api_key = settings.STRIPE_SECRET_KEY


def apply_coupon(request):
    if request.method == "POST" and request.is_ajax:
        input_code = request.POST.get('code')
        username = request.user.username
        try:
            use_code = OrdersDetail.objects.get(user__username=username, coupon__code=input_code)
            return JsonResponse({'data': 'exist'})
        except:
            try:
                coupon_code = CouponCode.objects.get(code=input_code)
                request.session['coupon_code'] = coupon_code.code
                return JsonResponse({'data': 'success'})
            except:
                return JsonResponse({'data': 'does not exist'})
    return JsonResponse({'data': 'error'})


def order_details(request):
    delivery_id = request.session['address_id']
    username = request.user.username
    order_items = CartItem.objects.filter(user__username=username)
    address_qs = AddressManage.objects.filter(id=delivery_id)
    sub_total = request.session['sub_total']
    delivery_charge = request.session['delivery_charge']
    total = request.session['total']

    try:
        coupon = CouponCode.objects.get(code=request.session['coupon_code'])
        if total >= coupon.order_above:
            offer_discount = float(int(total * coupon.discount / 100))
            coupon_code = coupon.code
            total = total - offer_discount
    except KeyError:
        offer_discount = None
        coupon_code = None

    context = {
                'order_items': order_items,
                'sub_total': sub_total,
                'delivery_charge': delivery_charge,
                'offer_discount': offer_discount,
                'coupon_code': coupon_code,
                'total': total,
                'delivery_address': address_qs
               }

    return render(request, 'complete-order.html', context)


def payment_page(request):
    delivery_id = request.session['address_id']
    username = request.user.username
    order_items = CartItem.objects.filter(user__username=username)

    address_qs = AddressManage.objects.filter(id=delivery_id)
    total = request.session['total']
    key = settings.STRIPE_PUBLISHABLE_KEY
    context = {'order_items': order_items,
               'delivery_address': address_qs,
               'key': key,
               'total': total}

    return render(request, 'payment.html', context)


def send_payment(request):
    total = int(request.session['total']) * 100
    charge = stripe.Charge.create(
        amount=total,
        currency='inr',
        description='Payment Gateway Charge',
        source=request.POST['stripeToken']
    )
    print('Charge----------->', charge)
    stripe_id = charge['balance_transaction']
    amount = charge['amount'] / 100
    print('Amount------->', amount)
    username = request.user.username
    user_info = User.objects.get(username=username)
    delivery_id = request.session['address_id']
    address_qs = AddressManage.objects.get(id=delivery_id)
    print(address_qs)
    stripe_payment = PaymentDetails.objects.create(stripe_charge_id=stripe_id, user=user_info, amount=amount)
    print('Stripe_payment------->', stripe_payment)
    payment_details = PaymentDetails.objects.get(stripe_charge_id=stripe_id)
    order_summary = OrdersDetail()
    order_summary.user = user_info
    order_summary.address = address_qs
    order_summary.payment = payment_details
    try:
        coupon = CouponCode.objects.get(code=request.session['coupon_code'])
        order_summary.coupon = coupon
        order_summary.save()
    except:
        order_summary.save()

    print('order_summary---------------->', order_summary)
    order_items = CartItem.objects.filter(user__username=username)
    for items in order_items:
        product = items.product
        quantity = items.quantity
        price = items.price
        order = order_summary
        order_item = OrderItem.objects.create(product=product, quantity=quantity, price=price,
                                                 order=order)
    del request.session['coupon_code']
    return render(request, 'payment-success.html')
