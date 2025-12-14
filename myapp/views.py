# myapp/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db.models import Max
import csv
from datetime import timedelta
import random
from .models import Dht11, Incident


# Dashboard principal
def dashboard(request):
    dernier = Dht11.objects.order_by('-dt').first()
    incident_actif = Incident.objects.filter(resolu=False).first()

    context = {
        'dernier': dernier,
        'incident_actif': incident_actif,
    }
    return render(request, "dashboard.html", context)


# API POST depuis ESP8266
def api_post(request):
    if request.method == "POST":
        try:
            import json
            data = json.loads(request.body)
            temp = float(data.get("temp"))
            hum = float(data.get("hum"))

            Dht11.objects.create(temp=temp, hum=hum)
            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)


# Dernières valeurs pour mise à jour en temps réel (AJAX)
def latest_json(request):
    last = Dht11.objects.order_by('-dt').values('temp', 'hum', 'dt').first()
    if last:
        return JsonResponse(last)
    return JsonResponse({"temp": "--", "hum": "--", "dt": "--"})


# Graphique Température avec filtre date + export CSV
def graph_temp(request):
    debut = request.GET.get('debut')   # ex: 2025-12-13T10:00
    fin = request.GET.get('fin')

    donnees = Dht11.objects.all().order_by('dt')

    if debut:
        donnees = donnees.filter(dt__gte=debut)
    if fin:
        # Ajoute :59 pour inclure toute la minute sélectionnée
        fin_complete = fin + ":59"
        donnees = donnees.filter(dt__lte=fin_complete)

    # Export CSV si demandé
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="historique_temperature.csv"'
        writer = csv.writer(response)
        writer.writerow(['Date et heure', 'Température (°C)', 'Humidité (%)'])
        for d in donnees:
            writer.writerow([
                d.dt.strftime('%d/%m/%Y %H:%M'),
                d.temp,
                d.hum
            ])
        return response

    context = {
        'debut': debut,
        'fin': fin,
    }
    return render(request, "graph_temp.html", context)


# Graphique Humidité (même logique que température)
def graph_hum(request):
    debut = request.GET.get('debut')
    fin = request.GET.get('fin')

    donnees = Dht11.objects.all().order_by('dt')

    if debut:
        donnees = donnees.filter(dt__gte=debut)
    if fin:
        fin_complete = fin + ":59"
        donnees = donnees.filter(dt__lte=fin_complete)

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="historique_humidite.csv"'
        writer = csv.writer(response)
        writer.writerow(['Date et heure', 'Humidité (%)', 'Température (°C)'])
        for d in donnees:
            writer.writerow([
                d.dt.strftime('%d/%m/%Y %H:%M'),
                d.hum,
                d.temp
            ])
        return response

    context = {
        'debut': debut,
        'fin': fin,
    }
    return render(request, "graph_hum.html", context)


# Archive des incidents
def archive_incidents(request):
    incidents = Incident.objects.all().order_by('-date_debut')
    return render(request, "archive_incidents.html", {'incidents': incidents})


# Détail d’un incident
def detail_incident(request, pk):
    incident = get_object_or_404(Incident, pk=pk)

    if request.method == "POST":
        if 'resoudre' in request.POST:
            incident.resolu = True
            incident.date_fin = timezone.now()
        incident.commentaire = request.POST.get('commentaire', incident.commentaire)
        incident.accuse_reception = request.POST.get('accuse', incident.accuse_reception)
        incident.save()
        return redirect('detail_incident', pk=pk)

    return render(request, "detail_incident.html", {'incident': incident})


# SIMULATION de données chambre froide (à supprimer en production)
def simuler_donnees(request):
    Dht11.objects.all().delete()

    now = timezone.now()
    for i in range(50):
        dt = now - timedelta(minutes=20 * (50 - i))
        temp = round(random.uniform(2.5, 7.8), 1)
        hum = round(random.uniform(60, 85), 1)

        # Créer 2 pics d'incident pour tester
        if i in [10, 11]:
            temp = round(random.uniform(12, 16), 1)

        Dht11.objects.create(temp=temp, hum=hum, dt=dt)

    return JsonResponse({"status": "50 mesures de chambre froide simulées avec succès !"})