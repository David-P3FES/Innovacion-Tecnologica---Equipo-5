# billing/views.py
import stripe
from datetime import datetime, timezone

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from cuentas.models import Perfil  # ajusta si tu modelo vive en otro módulo

# --- Stripe API key ---
stripe.api_key = settings.STRIPE_SECRET_KEY


# ========== Utils ==========
def _ts_to_dt(ts: int):
    """Convierte timestamp (segundos) a datetime con tz UTC."""
    return datetime.fromtimestamp(ts, tz=timezone.utc)


def _activate_profile_from_session(session_obj: dict):
    """
    Marca al usuario como suscrito cuando Checkout termina (evento webhook).
    """
    meta = session_obj.get("metadata") or {}
    user_id = meta.get("user_id")
    if not user_id:
        return

    subscription_id = session_obj.get("subscription")
    customer_id = session_obj.get("customer")

    try:
        perfil = Perfil.objects.get(user_id=user_id)
        perfil.is_subscribed = True
        perfil.stripe_customer_id = customer_id
        perfil.stripe_subscription_id = subscription_id
        perfil.trial_ended = True  # si manejas trial interno

        if subscription_id:
            sub = stripe.Subscription.retrieve(subscription_id)
            perfil.stripe_current_period_end = _ts_to_dt(sub["current_period_end"])
        perfil.save()
    except Perfil.DoesNotExist:
        pass


def _update_period_from_invoice(invoice_obj: dict):
    """
    Para renovaciones: mantener period_end e is_subscribed (webhook).
    """
    subscription_id = invoice_obj.get("subscription")
    if not subscription_id:
        return
    try:
        perfil = Perfil.objects.get(stripe_subscription_id=subscription_id)
        sub = stripe.Subscription.retrieve(subscription_id)
        perfil.stripe_current_period_end = _ts_to_dt(sub["current_period_end"])
        perfil.is_subscribed = True
        perfil.save()
    except Perfil.DoesNotExist:
        pass


def _deactivate_from_subscription(sub_obj: dict):
    """
    Si se cancela/expira la suscripción, desactivar (webhook).
    """
    subscription_id = sub_obj.get("id")
    if not subscription_id:
        return
    try:
        perfil = Perfil.objects.get(stripe_subscription_id=subscription_id)
        perfil.is_subscribed = False
        perfil.save()
    except Perfil.DoesNotExist:
        pass


# ========== Checkout Session ==========
@require_POST
def create_checkout_session(request):
    """
    Crea la sesión de Checkout (modo suscripción) y devuelve session.url (JSON).
    Protegido por CSRF: tu fetch debe enviar X-CSRFToken.
    """
    plan = request.POST.get("plan", "monthly")

    price_id = {
        "weekly": settings.STRIPE_PRICE_ID_WEEKLY,
        "monthly": settings.STRIPE_PRICE_ID_MONTHLY,
        "yearly": settings.STRIPE_PRICE_ID_YEARLY,
    }.get(plan, settings.STRIPE_PRICE_ID_MONTHLY)

    # URLs absolutas con el MISMO host por el que llegó el usuario
    success_url = request.build_absolute_uri(reverse("billing:stripe_success")) + "?session_id={CHECKOUT_SESSION_ID}"
    cancel_url = request.build_absolute_uri(reverse("billing:stripe_cancel"))

    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{"price": price_id, "quantity": 1}],
            success_url=success_url,
            cancel_url=cancel_url,
            customer_email=request.user.email if request.user.is_authenticated else None,
            metadata={
                "user_id": request.user.id if request.user.is_authenticated else "",
                "plan": plan,
            },
            allow_promotion_codes=True,
            automatic_tax={"enabled": False},
        )
        return JsonResponse({"url": session.url})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


# ========== Customer Portal ==========
@require_POST
def create_customer_portal_session(request):
    """
    Crea sesión del Portal de Facturación para que el usuario gestione su suscripción.
    Espera POST con 'session_id' (el Checkout Session id).
    """
    try:
        checkout_session_id = request.POST.get("session_id")
        if not checkout_session_id:
            return JsonResponse({"error": "session_id requerido"}, status=400)

        checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)
        portal_session = stripe.billing_portal.Session.create(
            customer=checkout_session.customer,
            return_url=request.build_absolute_uri(reverse("billing:stripe_success")),
        )
        return JsonResponse({"url": portal_session.url})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def success_view(request):
    session_id = request.GET.get("session_id")
    if request.user.is_authenticated and session_id:
        try:
            sess = stripe.checkout.Session.retrieve(session_id)
            if str(sess.get("metadata", {}).get("user_id")) == str(request.user.id):
                sub_id = sess.get("subscription")
                cust_id = sess.get("customer")
                perfil = Perfil.objects.get(user=request.user)
                perfil.is_subscribed = True
                perfil.stripe_subscription_id = sub_id
                perfil.stripe_customer_id = cust_id
                if sub_id:
                    sub = stripe.Subscription.retrieve(sub_id)
                    perfil.stripe_current_period_end = datetime.fromtimestamp(
                        sub["current_period_end"], tz=timezone.utc
                    )
                perfil.trial_ended = True
                perfil.save()
        except Exception as e:
            print("Error en success_view:", e)

    # 🔁 Al terminar, redirige directamente al panel
    return redirect("publicaciones:panel")

def cancel_view(request):
    return render(request, "billing/cancel.html")


# ========== Webhook ==========
@csrf_exempt  # Stripe no envía CSRF; este endpoint DEBE estar exento
def stripe_webhook(request):
    """
    Webhook: valida firma y procesa eventos.
    Configura STRIPE_WEBHOOK_SECRET en tus variables de entorno.
    """
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=sig_header, secret=endpoint_secret
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    etype = event.get("type")
    data = event.get("data", {}).get("object", {})

    if etype == "checkout.session.completed":
        _activate_profile_from_session(data)

    elif etype == "invoice.payment_succeeded":
        _update_period_from_invoice(data)

    elif etype in (
        "customer.subscription.deleted",
        "customer.subscription.canceled",
        "customer.subscription.paused",
    ):
        _deactivate_from_subscription(data)

    return HttpResponse(status=200)
