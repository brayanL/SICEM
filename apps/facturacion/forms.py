__author__ = 'ronald'
from django.forms import ModelForm, TextInput, NumberInput
from .models import Autorizacion, FacturaVenta
from apps.actores.forms import Controles


class AutorizacionForm(ModelForm):

    class Meta:
        model = Autorizacion
        fields = '__all__'
        widgets = {
            'autorizacion_sri' : TextInput(attrs={"class":"form-control",  "required":"required"}),
            'nro_establecimiento' : NumberInput(attrs={"class":"form-control",  "required":"required"}),
            'nro_emision' : NumberInput(attrs={"class":"form-control",  "required":"required"}),
        }
