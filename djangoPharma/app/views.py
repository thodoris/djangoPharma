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
        user_form = UserForm(data=request.POST,prefix="user")
        address_form = UserAddressForm(data=request.POST,prefix="address")

        if user_form.is_valid() and address_form.is_valid():
            new_user=user_form.save()
            UserAddress.objects.create(user=new_user, street=address_form.cleaned_data['street'],streetno=address_form.cleaned_data['streetno'] , city=address_form.cleaned_data['city'] , zip = address_form.cleaned_data['zip'])
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


def add_to_cart(request):
    # hardcoded values TODO remove
    # product = restService.get_drug_by_id('000090201')
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


def remove_from_cart(request):
    # hardcoded values TODO remove
    drug = DrugModel.objects.get(id='1')
    cart = Cart(request)
    cart.remove(drug)


def get_cart(request):
    return render_to_response('app/cart.html', dict(cart=Cart(request)))


def get_orders(request):
    if request.method == 'GET':
        user = User.objects.get(pk=2)
        orders = Order.objects.get(user=user)
        return render_to_response('app/orders.html', dict(orders=orders))
    elif request.method == 'POST':
        cart = Cart(request)
        user = User.objects.get(pk=3)
        address = UserAddress.objects.get(pk=3)
        order_date = datetime.datetime.now()
        status = '1'
        payment_type = '1'
        shipment_type = '1'
        comments = 'commmmments'

        order = Order.objects.create(user=user, address=address, order_date=order_date,
                                     status=status, payment_type=payment_type, shipment_type=shipment_type,
                                     comments=comments)

        for item in cart.cart.item_set.all():
            quantity = item.quantity
            unit_price = item.total_price
            drug = item.product
            order_details = OrderDetails.objects.create(order=order, drug=drug,
                                                        quantity=quantity, unit_price=unit_price)
