# publicaciones/forms.py
from django import forms
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from .models import Publicacion, FotoPublicacion

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        exclude = ("usuario",)
        widgets = {
            "titulo": forms.TextInput(attrs={"placeholder": "Título breve", "class": "input-text"}),
            "descripcion": forms.Textarea(attrs={"rows": 4, "placeholder": "Describe la propiedad", "class": "input-textarea"}),

            "precio": forms.NumberInput(attrs={"step": "0.01", "placeholder": "0.00", "class": "input-number"}),
            "tipo_operacion": forms.Select(attrs={"class": "input-select"}),
            "tipo_financiamiento": forms.Select(attrs={"class": "input-select"}),

            "recamaras": forms.NumberInput(attrs={"min": 0, "class": "input-number"}),
            "banos": forms.NumberInput(attrs={"step": "0.5", "min": 0, "class": "input-number"}),
            "estacionamientos": forms.NumberInput(attrs={"min": 0, "class": "input-number"}),
            "metros_construccion": forms.NumberInput(attrs={"min": 0, "class": "input-number"}),
            "metros_terreno": forms.NumberInput(attrs={"min": 0, "class": "input-number"}),

            "calle": forms.TextInput(attrs={"placeholder": "Calle", "class": "input-text dir-input"}),
            "numero": forms.TextInput(attrs={"placeholder": "Número (opcional)", "class": "input-text dir-input"}),
            "codigo_postal": forms.TextInput(attrs={"placeholder": "CP (5 dígitos)", "class": "input-text dir-input"}),
            "colonia": forms.TextInput(attrs={"placeholder": "Colonia", "class": "input-text dir-input"}),
            "ciudad": forms.TextInput(attrs={"placeholder": "Ciudad", "class": "input-text dir-input"}),
            "estado": forms.TextInput(attrs={"placeholder": "Estado", "class": "input-text dir-input"}),

            "estatus": forms.Select(attrs={"class": "input-select"}),

            "latitud": forms.HiddenInput(),
            "longitud": forms.HiddenInput(),
        }

    def clean(self):
        cleaned = super().clean()
        lat = cleaned.get("latitud")
        lon = cleaned.get("longitud")
        if lat is None or lon is None:
            raise forms.ValidationError("Coloca el marcador en el mapa o usa el buscador para fijar la ubicación.")
        return cleaned


class _BaseFotoFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        total = 0

        for form in self.forms:
            if not hasattr(form, "cleaned_data"):
                continue
            if form.cleaned_data.get("DELETE"):
                continue

            tiene_instancia = bool(getattr(form.instance, "pk", None) and form.instance.imagen)
            tiene_imagen_nueva = bool(form.cleaned_data.get("imagen"))
            if tiene_imagen_nueva or tiene_instancia:
                total += 1

        if total < 1:
            raise forms.ValidationError("Debes subir al menos una foto.")

# Permitimos 0..N portadas; luego normalizamos en la vista
FotoPublicacionFormSet = inlineformset_factory(
    parent_model=Publicacion,
    model=FotoPublicacion,
    fields=("imagen", "es_portada", "orden"),
    extra=3,
    can_delete=True,
    formset=_BaseFotoFormSet,
)
