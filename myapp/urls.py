from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('temperature/', views.graph_temp, name='graph_temp'),
    path('humidity/', views.graph_hum, name='graph_hum'),
    path('latest_json/', views.latest_json, name='latest_json'),
    path('api/post', views.api_post, name='api_post'),
]
