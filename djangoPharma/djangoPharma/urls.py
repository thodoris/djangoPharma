"""
Definition of urls for djangoPharma.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views
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
    url(r'^add_from_cart$', app.views.add_to_cart, name='add_from_cart'),
    url(r'^remove_from_cart$', app.views.remove_from_cart, name='remove_from_cart'),
]
