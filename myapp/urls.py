from django.urls import path
from . import views
from .api import Dlist, Dhtviews  # <-- ajoute cette ligne

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('temperature/', views.graph_temp, name='graph_temp'),
    path('humidity/', views.graph_hum, name='graph_hum'),
    path('latest_json/', views.latest_json, name='latest_json'),
    path('api/post', views.api_post, name='api_post'),

    # API DRF pour les graphiques
    path('api/dlist/', Dlist, name='dlist'),
    path('api/dht11/', Dhtviews.as_view()),
     #incidents
path('incidents/', views.archive_incidents, name='archive_incidents'),
path('incident/<int:pk>/', views.detail_incident, name='detail_incident'),


]