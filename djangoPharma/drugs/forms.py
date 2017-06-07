from django.forms import ModelForm
from .models import Drug, Category
from django import forms
from django.utils.translation import ugettext_lazy as _
from .validators import validate_integer
import json
from django.core.validators import RegexValidator


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class AddDrugsForm(ModelForm):
    id = forms.CharField(label=_("Drug ID"), required=True, max_length=254,
                         widget=forms.TextInput({
                             'class': 'form-control',
                             'placeholder': 'Drug ID'}))

    friendly_name = forms.CharField(label=_("Friendly Name"), required=True, max_length=254,
                                    widget=forms.TextInput({
                                        'class': 'form-control',
                                        'placeholder': 'Friendly name'}))

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
                                   'placeholder': 'Price'}))

    category = UserModelChoiceField(queryset=Category.objects.all(), widget=forms.Select({
        'class': 'form-control',
        'placeholder': 'Category'}))

    class Meta:
        model = Drug
        fields = ['id', 'friendly_name', 'availability', 'description', 'price', 'category']

        # def __init__(self, *args, **kwargs):
        # drug_categories = kwargs.pop('drug_categories')
        # all_drugs = kwargs.pop('all_drugs')
        # super(AddDrugsForm, self).__init__(*args, **kwargs)
        # decoded_json = json.loads(drug_categories)
        # self.fields['category'] = forms.ChoiceField(label='Category Name',
        #                                             widget=forms.Select(attrs={'class': 'form-control'}),
        #                                             choices=[(x['id'], x['name']) for x in
        #                                                      decoded_json['drugCategory']])
        #
        # self.fields['drug_id'] = forms.ChoiceField(label='Drug ID',
        #                                            widget=forms.Select(attrs={'class': 'form-control',
        #                                                                       'placeholder': 'Drug ID'}),
        #                                            choices=[('1000', '1000')])
        # choices=[(x['id'], x['id']) for x in all_drugs])


class UpdateDrugsForm(ModelForm):
    drug_id = forms.CharField(label=_("Drug ID"), required=True, max_length=254,
                              widget=forms.TextInput({
                                  'class': 'form-control',
                                  'placeholder': 'Drug ID'}))

    friendly_name = forms.CharField(label=_("Friendly Name"), required=True, max_length=254,
                                    widget=forms.TextInput({
                                        'class': 'form-control',
                                        'placeholder': 'Friendly name'}))

    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

    availability = forms.IntegerField(validators=[alphanumeric], label=_("Availability"), required=True,
                                      widget=forms.TextInput({
                                          'class': 'form-control',
                                          'placeholder': 'Availability'}))

    description = forms.CharField(label=_("Description"), required=True, max_length=254,
                                  widget=forms.TextInput({
                                      'class': 'form-control',
                                      'placeholder': 'Description'}))

    class Meta:
        model = Drug
        fields = ['id', 'friendly_name', 'availability', 'description']

    def __init__(self, *args, **kwargs):
        drug_categories = kwargs.pop('drug_categories')
        # all_drugs = kwargs.pop('all_drugs')
        super(UpdateDrugsForm, self).__init__(*args, **kwargs)
        decoded_json = json.loads(drug_categories)
        # self.initial['category_id'] = 'default value'
        self.fields['category'] = forms.ChoiceField(label='Category Name',
                                                    widget=forms.Select(attrs={'class': 'form-control'}),
                                                    choices=[(x['id'], x['name']) for x in
                                                             decoded_json['drugCategory']])
        # set the saved value
        self.fields['category'].initial = [self.initial['category_id']]

        # self.fields['drug_id'] = forms.ChoiceField(label='Drug ID',
        #                                            widget=forms.Select(attrs={'class': 'form-control',
        #                                                                       'placeholder': 'Drug ID'}),
        #                                            choices=[('1000', '1000')])
        # choices=[(x['id'], x['id']) for x in all_drugs])
