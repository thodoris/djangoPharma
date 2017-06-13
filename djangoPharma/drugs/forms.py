from django import forms
from django.core.validators import RegexValidator
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import Drug, Category


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class AddDrugsForm(ModelForm):
    id = forms.CharField(label=_("Drug ID"), required=True, max_length=254,
                         widget=forms.TextInput({
                             'class': 'form-control',
                             'placeholder': 'Drug ID',
                             'readonly': 'readonly'}))

    friendly_name = forms.CharField(label=_("Friendly Name"), required=True, max_length=254,
                                    widget=forms.TextInput({
                                        'class': 'form-control',
                                        'placeholder': 'Friendly name',
                                        'readonly': 'readonly'}))

    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

    availability = forms.IntegerField(validators=[alphanumeric], label=_("Availability"), required=True,
                                      widget=forms.TextInput({
                                          'class': 'form-control',
                                          'placeholder': 'Availability'}))

    description = forms.CharField(label=_("Description"), required=True, max_length=254,
                                  widget=forms.TextInput({
                                      'class': 'form-control',
                                      'placeholder': 'Description'}))

    price = forms.DecimalField(label=_("Price"), required=True, max_digits=5, decimal_places=2,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Price',
                                   'readonly': 'readonly'}))

    category = UserModelChoiceField(queryset=Category.objects.all(), widget=forms.Select({
        'class': 'form-control',
        'placeholder': 'Category'}))

    error_css_class = 'error'

    class Meta:
        model = Drug
        fields = ['id', 'friendly_name', 'availability', 'description', 'price', 'category']

    def __init__(self, *args, **kwargs):
        categoryChoices = kwargs.pop("categorychoices")  # categorychoices is the parameter passed from views.py
        category = kwargs.pop("category")
        super(AddDrugsForm, self).__init__(*args, **kwargs)
        if category is not None:
            self.category = kwargs.pop(category, None)
        if categoryChoices is not None:
            self.fields['category'] = forms.ChoiceField(label="Category", choices=categoryChoices, widget=forms.Select({
                'class': 'form-control',
                'placeholder': 'Category'}))


class UpdateDrugsForm(ModelForm):
    id = forms.CharField(label=_("Drug ID"), required=True, max_length=254,
                         widget=forms.TextInput({
                             'class': 'form-control',
                             'placeholder': 'Drug ID',
                             'readonly': 'readonly'}))

    friendly_name = forms.CharField(label=_("Friendly Name"), required=True, max_length=254,
                                    widget=forms.TextInput({
                                        'class': 'form-control',
                                        'placeholder': 'Friendly name',
                                        'readonly': 'readonly'}))

    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

    availability = forms.IntegerField(validators=[alphanumeric], label=_("Availability"), required=True,
                                      widget=forms.TextInput({
                                          'class': 'form-control',
                                          'placeholder': 'Availability'}))

    description = forms.CharField(label=_("Description"), required=True, max_length=254,
                                  widget=forms.TextInput({
                                      'class': 'form-control',
                                      'placeholder': 'Description'}))

    price = forms.DecimalField(label=_("Price"), required=True, max_digits=5, decimal_places=2,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Price',
                                   'readonly': 'readonly'}))

    category = UserModelChoiceField(queryset=Category.objects.all(), widget=forms.Select({
        'class': 'form-control',
        'placeholder': 'Category'}))

    class Meta:
        model = Drug
        fields = ['id', 'friendly_name', 'availability', 'description', 'price', 'category']

    def __init__(self, *args, **kwargs):
        categoryChoices = kwargs.pop("categorychoices")  # categorychoices is the parameter passed from views.py
        super(UpdateDrugsForm, self).__init__(*args, **kwargs)
        # self.fields['category'] = forms.ChoiceField(label="Category", choices=categoryChoices,widget=forms.Select({
        # 'class': 'form-control',
        # 'placeholder': 'Category'}))
