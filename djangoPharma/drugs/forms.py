from django.forms import ModelForm
from .models import Drug
from django import forms
from django.utils.translation import ugettext_lazy as _
from .validators import validate_integer
import json
from django.core.validators import RegexValidator


class AddDrugsForm(ModelForm):
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
        fields = ['drug_id', 'friendly_name', 'availability', 'description']

    def __init__(self, *args, **kwargs):
        drug_categories = kwargs.pop('drug_categories')
        all_drugs = kwargs.pop('all_drugs')
        super(AddDrugsForm, self).__init__(*args, **kwargs)
        decoded_json = json.loads(drug_categories)
        self.fields['category'] = forms.ChoiceField(label='Category Name',
                                                    widget=forms.Select(attrs={'class': 'form-control'}),
                                                    choices=[(x['id'], x['name']) for x in
                                                             decoded_json['drugCategory']])

        self.fields['drug_id'] = forms.ChoiceField(label='Drug ID',
                                              widget=forms.Select(attrs={'class': 'form-control',
                                                                         'placeholder': 'Drug ID'}),
                                              choices=[('1000', '1000')])
        # choices=[(x['id'], x['id']) for x in all_drugs])
