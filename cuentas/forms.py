# core/forms.py
from django import forms
from django.contrib.auth import get_user_model
from .models import Perfil

User = get_user_model()

class CompleteProfileForm(forms.ModelForm):
    # Campos del User
    username   = forms.CharField(max_length=150, required=True, label='Usuario')
    first_name = forms.CharField(max_length=150, required=True, label='Nombre')
    last_name  = forms.CharField(max_length=150, required=True, label='Apellido')
    email      = forms.EmailField(required=True, label='Email')

    class Meta:
        model = Perfil
        fields = ['rfc', 'whatsapp']   # RFC y WhatsApp del Perfil

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        # Prefill desde User
        self.fields['username'].initial   = self.user.username
        self.fields['first_name'].initial = self.user.first_name
        self.fields['last_name'].initial  = self.user.last_name
        self.fields['email'].initial      = self.user.email

        # Placeholders visuales
        self.fields['rfc'].widget.attrs.update({"placeholder": "Ejemplo: GODE561231GR8"})
        self.fields['whatsapp'].widget.attrs.update({"placeholder": "+5216561234567"})

    # =======================
    # Validaciones personalizadas
    # =======================
    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError('Este nombre de usuario ya existe.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError('Este email ya está registrado.')
        return email

    def clean_rfc(self):
        rfc = (self.cleaned_data.get('rfc') or '').strip().upper()
        return rfc  # El validador del modelo se encarga del formato

    def clean_whatsapp(self):
        whatsapp = (self.cleaned_data.get('whatsapp') or '').strip()
        return whatsapp  # El validador del modelo se encarga del formato

    # =======================
    # Guardar
    # =======================
    def save(self, commit=True):
        perfil = super().save(commit=False)

        # Actualiza datos del User
        self.user.username   = self.cleaned_data['username']
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name  = self.cleaned_data['last_name']
        self.user.email      = self.cleaned_data['email']

        if commit:
            self.user.save()
            perfil.user = self.user
            perfil.save()
        return perfil
