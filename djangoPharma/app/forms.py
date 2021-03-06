"""
Definition of forms.
"""

from app.models import UserAddress
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationForm


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
    first_name = forms.CharField(label=_("First name"), required=False, max_length=254,
                                 widget=forms.TextInput({
                                     'class': 'form-control',
                                     'placeholder': 'First name'}))
    last_name = forms.CharField(label=_("Last name"), required=False, max_length=254,
                                widget=forms.TextInput({
                                    'class': 'form-control',
                                    'placeholder': 'Last name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')





class UserProfileForm(forms.ModelForm):
    """Form for UserProfile"""
    class Meta:
        model = User
        fields = ( 'email', 'first_name', 'last_name')


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ('street', 'streetno', 'city', 'zip')



class ContactForm(forms.Form):
    contact_email = forms.EmailField(required=True, label=_("Email"),
                                     widget=forms.EmailInput({
                                         'class': 'form-control',
                                         'placeholder': 'Email'}))
    content = forms.CharField(label=_("Your Message"), required=True, max_length=999,
                              widget=forms.Textarea({
                                  'class': 'form-control',
                                  'placeholder': 'Your Message'}))
