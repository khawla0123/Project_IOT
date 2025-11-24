from django.shortcuts import render
from django.http import JsonResponse
from .models import Dht11

# Dashboard principal
def dashboard(request):
    return render(request, "dashboard.html")

# API Arduino POST
def api_post(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        temp = data.get("temp")
        hum = data.get("hum")
        from datetime import datetime
        dt = datetime.now()
        Dht11.objects.create(temp=temp, hum=hum, dt=dt)
        return JsonResponse({"status": "ok"})
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

# API GET pour le dashboard
def latest_json(request):
    last = Dht11.objects.order_by('-dt').values('temp', 'hum', 'dt').first()
    if last:
        return JsonResponse(last)
    else:
        return JsonResponse({"temp": "--", "hum": "--", "dt": "--"})

# Placeholder pour le graphe température
def graph_temp(request):
    return render(request, "graph_temp.html")  # crée ce template si besoin

# Placeholder pour le graphe humidité
def graph_hum(request):
    return render(request, "graph_hum.html")  # crée ce template si besoin
