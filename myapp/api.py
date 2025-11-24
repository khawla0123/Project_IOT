from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import Dht11
from .serializers import DHT11serialize
from .utils import send_telegram


@api_view(['GET'])
def Dlist(request):
    data_all = Dht11.objects.all().order_by('-dt')
    serializer = DHT11serialize(data_all, many=True)
    return Response({"data": serializer.data})


class Dhtviews(generics.CreateAPIView):
    queryset = Dht11.objects.all()
    serializer_class = DHT11serialize

    def perform_create(self, serializer):
        instance = serializer.save()
        temp = instance.temp

        # Email optionnel
        if temp > 25:
            try:
                send_mail(
                    "Alerte Température élevée",
                    f"Température = {temp}°C à {instance.dt}",
                    settings.EMAIL_HOST_USER,
                    ["test@test.com"],
                    fail_silently=True
                )
            except:
                pass

            # Telegram
            msg = f"⚠️ Alerte: {temp}°C (>25) à {instance.dt}"
            send_telegram(msg)
