from django.db import models
from django.utils import timezone

class Dht11(models.Model):
    temp = models.FloatField()
    hum = models.FloatField()
    dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.temp}°C - {self.hum}% - {self.dt}"

class Incident(models.Model):
    date_debut = models.DateTimeField(default=timezone.now)
    date_fin = models.DateTimeField(null=True, blank=True)
    compteur_alerte = models.IntegerField(default=0)
    temperature_max = models.FloatField(default=0)
    resolu = models.BooleanField(default=False)
    commentaire = models.TextField(blank=True)
    accuse_reception = models.TextField(blank=True)

    def duree(self):
        if self.date_fin:
            return self.date_fin - self.date_debut
        return timezone.now() - self.date_debut

    def est_grave(self):
        return self.duree().total_seconds() > 10 * 3600  # > 10 heures

    def etat(self):
        if self.resolu:
            return "vert"
        return "rouge" if self.est_grave() else "orange"

    def __str__(self):
        return f"Incident {self.id} - {self.date_debut.strftime('%d/%m %H:%M')}"