from datetime import datetime

import drugs.migrationService as migrationService
import drugs.models as DrugModel
from cart.cart import Cart
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect

from .models import Order, OrderDetails
from .models import UserAddress


def check_admin(user):
    return user.is_superuser


def syncdb(request):
    """Renders the home page."""
    result = migrationService.synchronize_data()
    data = {
        'result': result
    }
    if data['result'] is None:
        data['error_message'] = 'An error occurred while synchronizing local DB'
    return JsonResponse(data)


@login_required()
def add_to_cart(request):
    if request.method == 'POST':
        try:
            drug_id = request.POST.get('drug_id', '')
            quantity = request.POST.get('quantity', '')
            drug = DrugModel.Drug.objects.get(pk=drug_id)
            cart = Cart(request)
            # args: model, price, quantity
            cart.add(drug, drug.price, quantity)
            # everything went correct
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(status=500)
    else:
        # home page
        return redirect('/')


# ----------- cart ajax calls -------------------

@login_required()
def update_cart(request):
    if request.method == 'POST':
        try:
            drug_id = request.POST.get('drug_id', '')
            quantity = request.POST.get('quantity', '')
            drug = DrugModel.Drug.objects.get(id=drug_id)
            cart = Cart(request)
            # args: model, price, quantity
            cart.update(drug, quantity, drug.price)
            # everything went correct
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(status=500)
    else:
        # home page
        return redirect('/')


@login_required()
def remove_from_cart(request):
    if request.method == 'POST':
        try:
            drug_id = request.POST.get('drug_id', '')
            drug = DrugModel.Drug.objects.get(id=drug_id)
            cart = Cart(request)
            cart.remove(drug)
            # everything went correct
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(status=500)
    else:
        # home page
        return redirect('/')


# ----------- order ajax calls -------------------

@login_required()
def submit_order(request):
    if request.method == 'POST':
        current_user = request.user
        current_user_address = UserAddress.objects.get(user=current_user)
        order_date = datetime.now()
        shipment_type = request.POST.get('shipmentType', '')
        payment_type = request.POST.get('paymentType', '')
        comments = request.POST.get('comments', '')
        # submitted status
        status = '2'
        try:
            with transaction.atomic():
                # save order
                order = Order.objects.create(user=current_user, address=current_user_address, order_date=order_date,
                                             status=status, payment_type=payment_type, shipment_type=shipment_type,
                                             comments=comments)
                # save order details
                cart = Cart(request)
                for item in cart.cart.item_set.all():
                    quantity = item.quantity
                    total_price = item.total_price
                    drug = item.product
                    order_details = OrderDetails.objects.create(order=order, drug=drug,
                                                                quantity=quantity, total_price=total_price)
                # clear the cart
                cart.clear()
        except Exception as e:
            return HttpResponse(status=500)

        return HttpResponse(status=200)
    else:
        # home page
        return redirect('/')


@user_passes_test(check_admin)
def update_customer_order(request):
    if request.method == 'POST':
        try:
            order_id = request.POST.get('order_id', '')
            status = request.POST.get('status', '')
            # fetch the model from database
            order = Order.objects.get(pk=order_id)
            # update only status field
            order.status = status
            order.save(update_fields=["status"])
            return HttpResponse(status=200)
        except Exception:
            return HttpResponse(status=500)
    else:
        # home page
        return redirect('/')
