from rest_framework import generics
from django.utils import timezone

from .models import Dht11, Incident, Operateur, AccuseReception
from .serializers import DHT11serialize
from .utils import envoyer_alerte_email

from django.http import JsonResponse

# compteur_alerte → niveau opérateur
SEUILS_ESCALADE = {
    1: 1,   # dès la 1ère alerte → niveau 1
    4: 2,   # à 4 alertes → niveau 2
    7: 3,   # à 7 alertes → niveau 3
}


class Dhtviews(generics.CreateAPIView):
    queryset = Dht11.objects.all()
    serializer_class = DHT11serialize

    def perform_create(self, serializer):
        instance = serializer.save()
        temp = instance.temp
        hum = instance.hum

        print(f"[DHT11] Mesure reçue → Temp={temp}°C | Hum={hum}%")

        # 🔴 TEMPÉRATURE HORS PLAGE
        if temp < 2 or temp > 8:
            incident = Incident.objects.filter(resolu=False).first()

            # incident existant
            if incident:
                incident.compteur_alerte += 1
                incident.temperature_max = max(incident.temperature_max, temp)
                incident.save()

            # nouvel incident
            else:
                incident = Incident.objects.create(
                    compteur_alerte=1,
                    temperature_max=temp,
                    resolu=False
                )

            # 🔔 Escalade selon compteur
            niveau = SEUILS_ESCALADE.get(incident.compteur_alerte)

            if niveau:
                operateurs = Operateur.objects.filter(niveau=niveau)

                for operateur in operateurs:
                    AccuseReception.objects.get_or_create(
                        incident=incident,
                        operateur=operateur
                    )

                # 📧 ENVOI EMAIL (APRES création des accusés)
                envoyer_alerte_email(incident)

        # 🟢 TEMPÉRATURE NORMALE → CLÔTURE INCIDENT
        else:
            incident = Incident.objects.filter(resolu=False).first()
            if incident:
                incident.resolu = True
                incident.date_fin = timezone.now()
                incident.save()




