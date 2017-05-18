"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationForm
from app.models import UserAddress


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Password'}))


class UserForm(RegistrationForm):
    email = forms.EmailField(label=_("Email"), required=True, widget=forms.TextInput({
        'class': 'form-control',
        'placeholder': 'Email'}))
    first_name = forms.CharField(label=_("Firstname"), required=False, max_length=254,
                                 widget=forms.TextInput({
                                     'class': 'form-control',
                                     'placeholder': 'First name'}))
    last_name = forms.CharField(label=_("Lastname"), required=False, max_length=254,
                                widget=forms.TextInput({
                                    'class': 'form-control',
                                    'placeholder': 'Last name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ('street', 'streetno', 'city', 'zip')


class ContactForm(forms.Form):
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )
