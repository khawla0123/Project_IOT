from django.core.mail import send_mail
from django.conf import settings
from .models import Operateur


def operateurs_a_notifier(incident):
    operateurs = []

    if incident.compteur_alerte >= 1:
        operateurs += Operateur.objects.filter(niveau=1)

    if incident.compteur_alerte >= 4:
        operateurs += Operateur.objects.filter(niveau=2)

    if incident.compteur_alerte >= 7:
        operateurs += Operateur.objects.filter(niveau=3)

    return operateurs



def envoyer_alerte_email(incident):
    operateurs = operateurs_a_notifier(incident)

    emails = [op.user.email for op in operateurs if op.user.email]

    if not emails:
        return

    sujet = f"🚨 ALERTE TEMPÉRATURE – Incident #{incident.id}"

    message = f"""
🚨 Une alerte critique a été détectée.

Incident ID : {incident.id}
Température max : {incident.temperature_max} °C
Compteur alertes : {incident.compteur_alerte}

Merci de vous connecter au dashboard pour accuser réception.
"""

    send_mail(
        sujet,
        message,
        settings.DEFAULT_FROM_EMAIL,
        emails,
        fail_silently=False
    )
