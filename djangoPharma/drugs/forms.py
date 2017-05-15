from django.forms import ModelForm
from .models import Drug


class AddDrugsForm(ModelForm):
    class Meta:
        model = Drug
        fields = ['id', 'friendlyName', 'availability',  'description']
        managed = False
