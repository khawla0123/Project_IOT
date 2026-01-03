from django.urls import path
from . import views
from .api import Dhtviews
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('api/dht11/', Dhtviews.as_view(), name='api_dht11'),

    path('incidents/', views.archive_incidents, name='archive_incidents'),
    path('incident/<int:pk>/', views.detail_incident, name='detail_incident'),

    path('graph/temp/', views.graph_temp, name='graph_temp'),
    path('graph/hum/', views.graph_hum, name='graph_hum'),

    # Auth
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
     path(
    "logout/",
    auth_views.LogoutView.as_view(next_page="dashboard"),
    name="logout"
),
    # Opérateur / accusés
    path("mes-alertes/", views.mes_alertes, name="mes_alertes"),
    path("accuse/<int:pk>/", views.accuser_reception, name="accuser_reception"),

    # profile (login redirect)
    path("profile/", views.profile, name="profile"),

    # API pour récupérer la liste des mesures (JSON)
    path('api/dlist/', views.dht11_list, name='api_dlist'),

]
