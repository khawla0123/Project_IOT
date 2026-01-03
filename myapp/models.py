from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# --------------------
# Capteur DHT11
# --------------------
class Dht11(models.Model):
    temp = models.FloatField()
    hum = models.FloatField()
    dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.temp}°C - {self.hum}% - {self.dt}"


# --------------------
# Opérateurs
# --------------------
class Operateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    niveau = models.IntegerField()  # 1, 2, 3

    def __str__(self):
        return f"{self.user.username} (Niveau {self.niveau})"


# --------------------
# Incident
# --------------------
class Incident(models.Model):
    date_debut = models.DateTimeField(default=timezone.now)
    date_fin = models.DateTimeField(null=True, blank=True)

    compteur_alerte = models.IntegerField(default=0)
    temperature_max = models.FloatField(default=0)

    resolu = models.BooleanField(default=False)

    @property
    def etat(self):
        if self.resolu:
            return "vert"
        return "rouge"

    def __str__(self):
        return f"Incident #{self.id}"


# --------------------
# Accusé de réception
# --------------------
class AccuseReception(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE)
    operateur = models.ForeignKey(Operateur, on_delete=models.CASCADE)

    vu = models.BooleanField(default=False)
    commentaire = models.TextField(blank=True)

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("incident", "operateur")

    def __str__(self):
        return f"{self.operateur} - Incident {self.incident.id}"
