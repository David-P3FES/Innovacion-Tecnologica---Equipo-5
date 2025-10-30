"""
@file forms.py
@brief Formularios de la aplicación `cuentas`.
@details
 Contiene el formulario `CompleteProfileForm` usado para completar y actualizar
 la información de perfil de usuario, combinando datos del modelo `User` y del modelo `Perfil`.
"""

from django import forms
from django.contrib.auth import get_user_model
from .models import Perfil

#: Obtiene el modelo de usuario activo (CustomUser o User por defecto de Django)
User = get_user_model()


class CompleteProfileForm(forms.ModelForm):
    """
    @class CompleteProfileForm
    @brief Formulario para completar el perfil de un usuario.
    @details
     - Extiende de `forms.ModelForm` para trabajar con el modelo `Perfil`.
     - Incluye campos adicionales del modelo `User` (username, first_name, last_name, email).
     - Realiza validaciones personalizadas para evitar duplicados en username y email.
     - Actualiza datos tanto del `User` como del `Perfil` al guardar.
    """

    #: Campo de nombre de usuario
    username   = forms.CharField(max_length=150, required=True, label='Usuario')
    #: Campo de nombre
    first_name = forms.CharField(max_length=150, required=True, label='Nombre')
    #: Campo de apellido
    last_name  = forms.CharField(max_length=150, required=True, label='Apellido')
    #: Campo de correo electrónico
    email      = forms.EmailField(required=True, label='Email')

    class Meta:
        """
        @class Meta
        @brief Configuración del formulario ligada al modelo Perfil.
        """
        model = Perfil
        fields = ['rfc', 'whatsapp']   #: Campos específicos del modelo Perfil

    def __init__(self, *args, **kwargs):
        """
        @brief Inicializa el formulario con datos precargados del usuario.
        @param args Argumentos posicionales de ModelForm.
        @param kwargs Argumentos con parámetros extra (incluye `user`).
        """
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
        """
        @brief Valida que el nombre de usuario no esté duplicado.
        @return Nombre de usuario válido.
        @exception forms.ValidationError Si el username ya existe en otro usuario.
        """
        username = self.cleaned_data['username'].strip()
        if User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError('Este nombre de usuario ya existe.')
        return username

    def clean_email(self):
        """
        @brief Valida que el correo electrónico no esté duplicado.
        @return Email válido en minúsculas.
        @exception forms.ValidationError Si el email ya existe en otro usuario.
        """
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError('Este email ya está registrado.')
        return email

    def clean_rfc(self):
        """
        @brief Normaliza el RFC a mayúsculas.
        @return RFC en formato limpio.
        @note El validador del modelo `Perfil` se encarga de verificar el formato.
        """
        rfc = (self.cleaned_data.get('rfc') or '').strip().upper()
        return rfc

    def clean_whatsapp(self):
        """
        @brief Normaliza el número de WhatsApp.
        @return Número de WhatsApp en formato limpio.
        @note El validador del modelo `Perfil` se encarga de verificar el formato.
        """
        whatsapp = (self.cleaned_data.get('whatsapp') or '').strip()
        return whatsapp

    # =======================
    # Guardar
    # =======================
    def save(self, commit=True):
        """
        @brief Guarda los datos del perfil y actualiza también el modelo User.
        @param commit Si es True, se guardan los cambios en la base de datos.
        @return Objeto Perfil actualizado.
        """
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
