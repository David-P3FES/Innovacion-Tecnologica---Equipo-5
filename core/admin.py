# core/admin.py (o donde tengas el modelo de usuario)
from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

