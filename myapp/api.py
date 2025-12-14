# myapp/api.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics   # ←←← CETTE LIGNE MANQUAIT !!!
from django.core.mail import send_mail
from django.conf import settings
from .models import Dht11, Incident
from .serializers import DHT11serialize
from .utils import send_telegram
from django.utils import timezone


@api_view(['GET'])
def Dlist(request):
    data_all = Dht11.objects.all().order_by('-dt')
    serializer = DHT11serialize(data_all, many=True)
    return Response({"data": serializer.data})


class Dhtviews(generics.CreateAPIView):
    queryset = Dht11.objects.all()
    serializer_class = DHT11serialize

    def perform_create(self, serializer):
        instance = serializer.save()
        temp = instance.temp

        # === SYSTÈME D'INCIDENTS COMME TU VEUX ===
        incident_actif = Incident.objects.filter(resolu=False).first()

        # Température normale : 2°C < T < 8°C
        if 2 <= temp <= 8:
            if incident_actif:
                incident_actif.date_fin = timezone.now()
                incident_actif.resolu = True
                incident_actif.save()
        else:
            # Température anormale → incident
            if not incident_actif:
                incident_actif = Incident.objects.create(
                    temperature_max=temp,
                    compteur_alerte=1
                )
                send_telegram("ALERTE NIVEAU 1 : Température hors plage (2-8°C) ! Opérateur 1 requis.")
            else:
                incident_actif.compteur_alerte += 1
                incident_actif.temperature_max = max(incident_actif.temperature_max, temp)
                incident_actif.save()

                compteur = incident_actif.compteur_alerte
                if compteur == 4:
                    send_telegram("ALERTE NIVEAU 2 : Problème persistant ! Opérateur 2 requis.")
                elif compteur == 7:
                    send_telegram("ALERTE CRITIQUE : Opérateur 3 requis IMMÉDIATEMENT !")

                # Incident > 10 heures ?
                if (timezone.now() - incident_actif.date_debut).total_seconds() > 10 * 3600:
                    send_telegram("INCIDENT GRAVE > 10 HEURES ! Intervention urgente !")