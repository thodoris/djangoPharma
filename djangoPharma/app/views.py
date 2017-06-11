"""
Definition of views.
"""

from django.http import HttpRequest
from datetime import datetime
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

import drugs.cacheService as cacheService
from .forms import UserForm, UserAddressForm
from .forms import ContactForm
from cart.cart import Cart
from django.contrib.auth.models import User
from .models import UserAddress
from .models import Order, OrderDetails
import drugs.restService as restService
import drugs.models as DrugModel


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    drugs_data = cacheService.get_all_drugs()
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
        }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)

    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_email = request.POST.get('contact_email', '')
            form_content = request.POST.get('content', '')

        content = render_to_string('app/contact_info.txt', {
            'contact_email': contact_email,
            'form_content': form_content,
        })

        subject = 'Contact Info Message'
        from_address = 'e-pharmacy@no-reply.com'
        email = EmailMessage(subject, content, from_address, ['mymail@info.com'], headers={'Reply-To': contact_email})
        email.send()

        # return redirect('app/contact.html')

    return render(
        request,
        'app/contact.html',
        {
            'form': form_class,
            'title': 'Contact',
            'message': 'Your contact page.',
            'year': datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'About1',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        }
    )


def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST, prefix="user")
        address_form = UserAddressForm(data=request.POST, prefix="address")

        if user_form.is_valid() and address_form.is_valid():
            new_user = user_form.save()
            UserAddress.objects.create(user=new_user, street=address_form.cleaned_data['street'],
                                       streetno=address_form.cleaned_data['streetno'],
                                       city=address_form.cleaned_data['city'], zip=address_form.cleaned_data['zip'])
            return HttpResponseRedirect('/accounts/register/complete')
        else:
            return render(request, 'registration/registration_form.html', {'form': user_form})

    else:
        user_form = UserForm(prefix="user")
        address_form = UserAddressForm(prefix="address")
        context = {
            "user_form": user_form,
            "address_form": address_form
        }
        return render(request, 'registration/registration_form.html', context)


def registration_complete(request):
    return render('registration/registration_complete.html')


@login_required()
def add_to_cart(request):
    if request.method == 'POST':
        try:
            drug_id = request.POST.get('drug_id', '')
            quantity = request.POST.get('quantity', '')
            drug = DrugModel.Drug.objects.get(id=drug_id)
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


@login_required()
def update_cart(request):
    if request.method == 'POST':
        try:
            drug_id = request.POST.get('drug_id', '')
            quantity = request.POST.get('quantity', '')
            drug = DrugModel.Drug.objects.get(id=drug_id)
            cart = Cart(request)
            # args: model, price, quantity
            cart.update(drug, drug.price, quantity)
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


@login_required()
def get_cart(request):
    cart = Cart(request)
    return render(request, 'app/cart.html', dict(cart=cart))


@login_required()
def checkout(request):
    if request.method == 'POST' or True:
        cart = Cart(request)
        current_user = request.user
        current_user_address = UserAddress.objects.get(user=current_user)
        return render(request, 'app/checkout.html', dict(cart=cart, user=current_user, address=current_user_address))
    else:
        # home page
        return redirect('/')


@login_required()
def submit_order(request):
    if request.method == 'POST':
        current_user = request.user
        current_user_address = UserAddress.objects.get(user=current_user)
        order_date = datetime.now()
        shipment_type = request.POST.get('shipmentType', '')
        payment_type = request.POST.get('paymentType', '')
        comments = request.POST.get('comments', '')
        # submitted
        status = '2'
        # TODO put transaction for commit multiple insertions
        # save order
        order = Order.objects.create(user=current_user, address=current_user_address, order_date=order_date,
                                     status=status, payment_type=payment_type, shipment_type=shipment_type,
                                     comments=comments)
        # save order details
        cart = Cart(request)
        for item in cart.cart.item_set.all():
            quantity = item.quantity
            unit_price = item.total_price
            drug = item.product
            order_details = OrderDetails.objects.create(order=order, drug=drug,
                                                        quantity=quantity, unit_price=unit_price)

        return HttpResponse(200)
    else:
        # home page
        return redirect('/')


@login_required()
def get_orders(request):
    if request.method == 'GET':
        # TODO remove hardcoded
        user = User.objects.get(pk=1)
        orders = Order.objects.filter(user=user)
        return render(request, 'app/orders.html', dict(orders=orders))
