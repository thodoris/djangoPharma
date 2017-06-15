"""
Definition of urls for djangoPharma.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views
import app.ajaxviews
import drugs.urls

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin

import drugs

admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
    # include registration
    url(r'^accounts/register/$', app.views.register, name='register'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    # enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # include drugs application's urls
    url(r'^drugs/', include(drugs.urls)),
    url(r'^cart$', app.views.get_cart, name='get_cart'),
    url(r'^add_to_cart$', app.ajaxviews.add_to_cart, name='add_to_cart'),
    url(r'^update_cart', app.ajaxviews.update_cart, name='update_cart'),
    url(r'^remove_from_cart$', app.ajaxviews.remove_from_cart, name='remove_from_cart'),
    url(r'^my_orders$', app.views.get_orders, name='my_orders'),
    url(r'^my_orders/(?P<order_id>[0-9]+)/$', app.views.display_my_order, name='my_orders_display'),
    url(r'^checkout$', app.views.checkout, name='checkout'),
    url(r'^submit_order$', app.ajaxviews.submit_order, name='submit_order'),
    url(r'^order_result$', app.views.submit_order_result, name='submit_order_result'),
    url(r'^ajax/syncdb', app.ajaxviews.syncdb, name='syncdb'),
    url(r'^admin/orders$', app.views.get_customer_orders, name='customer_orders'),
    url(r'^admin/orders/(?P<order_id>[0-9]+)/$', app.views.display_order, name='display_order'),
    url(r'^admin/orders/update$', app.ajaxviews.update_customer_order, name='update_customer_order'),

]
