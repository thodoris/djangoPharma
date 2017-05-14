from django.forms import ModelForm
from .models import Drug


class AddDrugsForm(ModelForm):
    class Meta:
        model = Drug
        fields = ['id', 'friendlyname' , 'availability',  'description']
        managed = False
