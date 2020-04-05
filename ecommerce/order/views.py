import stripe
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render
from cart.models import CartItem
from .models import ManageAddress
from .models import Payment
from .models import OrderDetails

# Create your views here.


stripe.api_key = settings.STRIPE_SECRET_KEY


def order_details(request):
    delivery_id = request.session['address_id']
    username = request.user.username
    order_items = CartItem.objects.filter(user__username=username)
    address_qs = ManageAddress.objects.filter(id=delivery_id)
    sub_total = request.session['sub_total']
    delivery_charge = request.session['delivery_charge']
    total = request.session['total']

    context = {
                'order_items': order_items,
                'sub_total': sub_total,
                'delivery_charge': delivery_charge,
                'total': total,
                'delivery_address': address_qs
               }

    return render(request, 'complete-order.html', context)


def payment_page(request):
    delivery_id = request.session['address_id']
    username = request.user.username
    order_items = CartItem.objects.filter(user__username=username)
    items_id = []
    for i in order_items:
        items_id.append(str(i.id))

    item_id = ','.join(items_id)
    request.session['items_id'] = item_id
    address_qs = ManageAddress.objects.filter(id=delivery_id)
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
    stripe_id = charge['balance_transaction']
    amount = charge['amount']
    username = request.user.username
    user_info = User.objects.get(username=username)
    delivery_id = request.session['address_id']
    item_id = request.session['items_id']
    address_qs = ManageAddress.objects.get(id=delivery_id)
    print(address_qs)
    stripe_payment = Payment.objects.create(stripe_charge_id=stripe_id, user=user_info, amount=amount)
    payment_details = Payment.objects.get(stripe_charge_id=stripe_id)
    order_summary = OrderDetails.objects.create(user=user_info, order_items=item_id, ordered=True, address=address_qs, payment=payment_details, being_delivered=True)
    return render(request, 'payment-success.html')
