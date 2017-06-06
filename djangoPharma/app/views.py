"""
Definition of views.
"""

from django.http import HttpRequest
from datetime import datetime
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template import Context
from django.template.loader import get_template
from django.template.loader import render_to_string
from .forms import UserForm, UserAddressForm
from .forms import ContactForm
from cart.cart import Cart
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
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/register/complete')

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
    product = restService.get_drug_by_id('000090201')
    quantity = 1
    # set the model
    drug = DrugModel.Drug()
    drug.id = product['id']
    drug.friendly_name = product['name']
    # use only the one price from the two
    drug.price = product['price_retail']
    cart = Cart(request)
    # args: model, price, quantity
    cart.add(drug, drug.price, quantity)


def remove_from_cart(request):
    # hardcoded values TODO remove
    drug_id = '000090201'
    drug = DrugModel.Drug()
    drug.id = drug_id
    cart = Cart(request)
    cart.remove(drug)


def get_cart(request):
    return render_to_response('app/cart.html', dict(cart=Cart(request)))


def get_orders(request):
    return render_to_response('app/orders.html')
