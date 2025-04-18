from rest_framework import serializers
from sensorApp.models import Sensors

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sensors 
        fields=('sensorsId','temperature' , 'humidity' , 'air_quality' , 'timestamp')
