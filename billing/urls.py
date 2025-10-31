# billing/urls.py
from django.urls import path
from . import views

app_name = "billing"

urlpatterns = [
    path("create-checkout-session/", views.create_checkout_session, name="stripe_create_session"),
    path("success/", views.success_view, name="stripe_success"),
    path("cancel/", views.cancel_view, name="stripe_cancel"),
    path("create-portal-session/", views.create_customer_portal_session, name="stripe_portal_session"),
    path("webhook/", views.stripe_webhook, name="stripe_webhook"),
]
