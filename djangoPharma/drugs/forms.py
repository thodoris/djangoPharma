from django.forms import ModelForm
from .models import Drug
from django import forms


class AddDrugsForm(ModelForm):
    # name = forms.CharField(initial='class')
    days = forms.ChoiceField(choices=[(x, x) for x in range(1, 32)])

    class Meta:
        model = Drug
        fields = ['id', 'friendlyName', 'availability', 'description']
