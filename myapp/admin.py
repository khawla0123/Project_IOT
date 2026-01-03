from django.contrib import admin
from .models import Dht11, Operateur, Incident, AccuseReception

# DHT11
@admin.register(Dht11)
class Dht11Admin(admin.ModelAdmin):
    list_display = ('temp', 'hum', 'dt')
    list_filter = ('dt',)
    search_fields = ('temp', 'hum')

# Opérateurs
@admin.register(Operateur)
class OperateurAdmin(admin.ModelAdmin):
    list_display = ('user', 'niveau')
    search_fields = ('user__username',)

# Incidents
@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('id', 'temperature_max', 'compteur_alerte', 'resolu', 'date_debut', 'date_fin', 'etat')
    list_filter = ('resolu',)
    search_fields = ('id',)

# Accusés de réception
@admin.register(AccuseReception)
class AccuseReceptionAdmin(admin.ModelAdmin):
    list_display = ('incident', 'operateur', 'vu', 'date')
    list_filter = ('vu',)
    search_fields = ('incident__id', 'operateur__user__username')
