from django.db import models

class Dht11(models.Model):
    temp = models.FloatField()
    hum = models.FloatField()
    dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.temp} °C - {self.hum} %"

