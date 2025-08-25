from django import forms
from core.models import Perfil

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['rfc', 'rol', 'telefono', 'ciudad', 'estado']
