from django.db import models

# Create your models here.
class Sensors(models.Model):
    sensorsId = models.AutoField(primary_key=True)
    temperature = models.FloatField(default=4)
    humidity= models.FloatField(default=4)
    air_quality= models.FloatField(default=4)
    timestamp = models.DateTimeField()
