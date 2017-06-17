"""
Definition of views.
"""

from datetime import datetime

import drugs.cacheService as cacheService
from cart.cart import Cart
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string

from .forms import ContactForm
from .forms import UserForm, UserAddressForm
from .models import Order, OrderDetails
from .models import UserAddress


# check if the user is admin
def check_admin(user):
    return user.is_superuser


# check if the user is staff user
def check_back_office_user(user):
    return user.is_staff


# check if user is a simple user
def check_simple_user(user):
    return not user.is_staff


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    # get all drugs from the cache
    drugs_data = cacheService.get_all_drugs()
    if drugs_data is not None:
        context = {'data': drugs_data}
        return render(request, 'app/home.html', context)
    else:
        return render(request, 'app/error.html', {'error': 'Cannot get data', }, content_type='application/xhtml+xml')


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)

    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            # get the email and the message from the request
            contact_email = request.POST.get('contact_email', '')
            form_content = request.POST.get('content', '')
            try:
                content = render_to_string('app/contact_info.txt', {
                    'contact_email': contact_email,
                    'form_content': form_content,
                })

                subject = 'Contact Info Message'
                from_address = 'e-pharmacy@no-reply.com'
                email = EmailMessage(subject, content, from_address, ['mymail@info.com'],
                                     headers={'Reply-To': contact_email})
                # send the mail
                email.send()
                email_sent = True
            except Exception:
                email_sent = False

            return render(request, 'app/contact_result.html', dict(email_sent=email_sent))

    else:
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
@user_passes_test(check_simple_user)
def get_cart(request):
    # get cart
    cart = Cart(request)
    # check if cart is empty or not in order to display a warning message or the cart items
    cart_is_empty = cart.count() == 0
    return render(request, 'app/cart.html', dict(cart=cart, cart_is_empty=cart_is_empty))


@login_required()
@user_passes_test(check_simple_user)
def checkout(request):
    if request.method == 'POST':
        cart = Cart(request)
        # get logged in user
        current_user = request.user
        # get logged in user address
        current_user_address = UserAddress.objects.get(user=current_user)
        return render(request, 'app/checkout.html', dict(cart=cart, user=current_user, address=current_user_address))
    else:
        # home page
        return redirect('/')


@login_required()
@user_passes_test(check_simple_user)
def submit_order_result(request):
    if request.method == 'GET':
        # go to result page when the order has been submitted successfully
        return render(request, 'app/submit_order_result.html')


@login_required()
@user_passes_test(check_simple_user)
def get_orders(request):
    if request.method == 'GET':
        # get logged in user
        current_user = request.user
        orders = Order.objects.filter(user=current_user)
        return render(request, 'app/orders_list.html', dict(orders=orders))


@user_passes_test(check_back_office_user)
def get_customer_orders(request):
    if request.method == 'GET':
        # fetch all customer orders
        orders = Order.objects.all()
        return render(request, 'app/admin/orders_list.html', dict(orders=orders))


@user_passes_test(check_back_office_user)
def display_order(request, order_id):
    if request.method == 'GET':
        # fetch the specific order
        order = Order.objects.get(pk=order_id)
        # get order details
        order.attributes = OrderDetails.objects.filter(order_id=order.id)
        # get available statuses
        available_status_list = ()
        # according to the current status, only some or none status is available for later actions
        # when status is submitted (2), the back office user can update the status to 3 statuses
        if order.status == 2:
            available_status_list = ((3, 'Ready For Delivery'), (4, 'Delivered'), (5, 'Rejected'))
        elif order.status == 3:
            available_status_list = (4, 'Delivered'), (5, 'Rejected')
        return render(request, 'app/admin/edit_order.html', dict(order=order, statuses=available_status_list))


@login_required()
@user_passes_test(check_simple_user)
def display_my_order(request, order_id):
    if request.method == 'GET':
        # fetch specific order
        order = Order.objects.get(pk=order_id)
        # assign to the model also the one to many relationship order details
        order.attributes = OrderDetails.objects.filter(order_id=order.id)
        return render(request, 'app/display_order.html', dict(order=order))
