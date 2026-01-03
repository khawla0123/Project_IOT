from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Incident, Dht11, Operateur, AccuseReception

from django.http import JsonResponse
from .models import Dht11

def dashboard(request):
    incident_actif = Incident.objects.filter(resolu=False).first()
    dernier = Dht11.objects.order_by('-dt').first()

    accuse = None

    if request.user.is_authenticated and incident_actif:
        try:
            operateur = Operateur.objects.get(user=request.user)

            accuse, _ = AccuseReception.objects.get_or_create(
                incident=incident_actif,
                operateur=operateur
            )

            if request.method == "POST":
                accuse.vu = True
                accuse.commentaire = request.POST.get("commentaire", "")
                accuse.save()
                return redirect("dashboard")

        except Operateur.DoesNotExist:
            pass

    return render(request, "dashboard.html", {
        "incident_actif": incident_actif,
        "dernier": dernier,
        "accuse": accuse,
    })

def archive_incidents(request):
    incidents = Incident.objects.all().order_by("-date_debut")
    return render(request, "archive.html", {"incidents": incidents})


def detail_incident(request, pk):
    incident = get_object_or_404(Incident, id=pk)

    accuses = AccuseReception.objects.filter(
        incident=incident
    ).select_related("operateur__user")

    return render(request, "detail_incident.html", {
        "incident": incident,
        "accuses": accuses
    })


def graph_temp(request):
    return render(request, "graph_temp.html")


def graph_hum(request):
    return render(request, "graph_hum.html")


@login_required
def mes_alertes(request):
    """
    Liste des accusés pour l'opérateur connecté (page 'mes-alertes').
    """
    try:
        operateur = Operateur.objects.get(user=request.user)
    except Operateur.DoesNotExist:
        return redirect("dashboard")

    accuses = AccuseReception.objects.filter(operateur=operateur).select_related("incident").order_by("-date")
    return render(request, "mes_alertes.html", {"accuses": accuses})


@login_required
def accuser_reception(request, pk):
    """
    Page individuelle pour accuser + commenter (utilisée si on veut une page dédiée).
    Le paramètre pk correspond à l'id de l'AccuseReception.
    """
    accuse = get_object_or_404(AccuseReception, pk=pk)

    # sécurité : seul l'opérateur concerné peut marquer comme vu
    if accuse.operateur.user != request.user:
        return redirect("profile")

    if request.method == "POST":
        accuse.vu = True
        accuse.commentaire = request.POST.get("commentaire", "")
        accuse.save()
        return redirect("mes_alertes")  # ou "profile" selon ton choix

    return render(request, "accuser.html", {"accuse": accuse})


@login_required
def profile(request):
    """
    Page vers laquelle l'utilisateur est redirigé après login.
    Si c'est un opérateur, on lui affiche ses accusés + formulaire directement.
    """
    try:
        operateur = Operateur.objects.get(user=request.user)
    except Operateur.DoesNotExist:
        # Si ce n'est pas un opérateur, renvoyer vers le dashboard public
        return redirect("dashboard")

    # Création automatique d'accusés pour incidents actifs (optionnel)
    # On récupère tous les incidents actifs (ou décision: uniquement incident non résolu)
    incidents_actifs = Incident.objects.filter(resolu=False).order_by("-date_debut")
    for incident in incidents_actifs:
        AccuseReception.objects.get_or_create(incident=incident, operateur=operateur)

    accuses = AccuseReception.objects.filter(operateur=operateur).select_related("incident").order_by("-date")
    # Si post (accuser depuis profile)
    if request.method == "POST":
        accuse_id = request.POST.get("accuse_id")
        commentaire = request.POST.get("commentaire", "")
        accuse = get_object_or_404(AccuseReception, pk=accuse_id, operateur=operateur)
        accuse.vu = True
        accuse.commentaire = commentaire
        accuse.save()
        return redirect("profile")

    return render(request, "profile.html", {
        "operateur": operateur,
        "accuses": accuses
    })


def dht11_list(request):
    """
    Renvoie toutes les mesures DHT11 en JSON.
    """
    mesures = Dht11.objects.order_by('dt')
    data = [
        {"dt": m.dt.isoformat(), "temp": m.temp, "hum": m.hum}
        for m in mesures
    ]
    return JsonResponse({"data": data})
