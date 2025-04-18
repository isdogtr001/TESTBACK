import csv
from io import TextIOWrapper
from datetime import datetime
import pandas as pd

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt , csrf_protect
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse , HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views import View

from sensorApp.models import Sensors
from sensorApp.serializers import SensorSerializer



# Create your views here.
@csrf_exempt
def sensorsApi(request,id=0):
    if request.method=='GET':
        sensors = Sensors.objects.all()
        sensors_serializer=SensorSerializer(sensors,many=True)
        return JsonResponse(sensors_serializer.data,safe=False)
    elif request.method=='POST':
        sensors_data=JSONParser().parse(request)
        sensorss_serializer=SensorSerializer(data=sensors_data)
        if sensorss_serializer.is_valid():
            sensorss_serializer.save()
            return JsonResponse("Added Successfully",safe=False)
        return JsonResponse("Failed to Add",safe=False)
    elif request.method=='PUT':
        sensors_data=JSONParser().parse(request)
        sensors=Sensors.objects.get(sensorsId=sensors_data['sensorsId'])
        sensorss_serializer=SensorSerializer(sensors,data=sensors_data)
        if sensorss_serializer.is_valid():
            sensorss_serializer.save()
            return JsonResponse("Updated Successfully",safe=False)
        return JsonResponse("Failed to Update")
    elif request.method=='DELETE':
        sensors=Sensors.objects.get(sensorsId=id)
        sensors.delete()
        return JsonResponse("Deleted Successfully",safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CSVUploadView(View):
    def post(self, request):
        if 'file' not in request.FILES:
            return HttpResponseBadRequest("Missing file")

        file = request.FILES['file']
        decoded_file = TextIOWrapper(file, encoding='utf-8')
        reader = csv.DictReader(decoded_file)

        try:
            for row in reader:
               # Validate and convert temperature
                temperature = row['temperature'].strip()
                if temperature == '' or not temperature.replace('.', '', 1).isdigit():
                    temperature = None  # or you can set a default value (e.g., 0)

                # Validate and convert humidity
                humidity = row['humidity'].strip()
                if humidity == '' or not humidity.replace('.', '', 1).isdigit():
                    humidity = None  # or set a default value

                # Validate and convert air_quality
                air_quality = row['air_quality'].strip()
                if air_quality == '' or not air_quality.replace('.', '', 1).isdigit():
                    air_quality = None  # or set a default value

                # Validate and convert time
                timestamp = row['timestamp'].strip()
                try:
                    timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
                except ValueError:
                    timestamp = None  # or use a default value like `datetime.now()`

                if temperature is not None and humidity is not None and timestamp is not None and air_quality is not None:
                    Sensors.objects.create(
                        temperature=float(temperature),
                        humidity=float(humidity),
                        air_quality=float(air_quality),
                        timestamp=timestamp
                    )
                else:
                    # Log or handle the invalid row as needed
                    print(f"Skipping invalid row: {row}")

            return JsonResponse({'status': 'CSV data inserted'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@csrf_protect
class GetProcessed(View):
    def get_processed_sensor_data(request):
        if request.method != 'GET':
            return JsonResponse({"error": "Only GET allowed"}, status=405)

        queryset = Sensors.objects.all().values('temperature' , 'humidity' , 'air_quality' , 'timestamp')

        df = pd.DataFrame(list(queryset))
        if df.empty:
            return JsonResponse({"message": "No sensor data found."}, status=404)

        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)

        # Z-score anomaly detection for each sensor metric
        for col in ['temperature', 'humidity', 'air_quality']:
            mean = df[col].mean()
            std = df[col].std()
            df[f'{col}_z'] = (df[col] - mean) / std
            df[f'{col}_anomaly'] = df[f'{col}_z'].abs() > 2

        df.drop(columns=[col for col in df.columns if col.endswith('_z')], inplace=True)

        return JsonResponse(df.to_dict(orient='records'), safe=False)

@csrf_protect
class GetAggregated(View):
    def get_aggregated_sensor_data(request):
        if request.method != 'GET':
            return JsonResponse({"error": "Only GET allowed"}, status=405)

        queryset = Sensors.objects.all().values('temperature', 'humidity', 'air_quality')
        df = pd.DataFrame(list(queryset))

        if df.empty:
            return JsonResponse({"message": "No sensor data found."}, status=404)

        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)

        # Calculate aggregates
        stats = {}
        for col in ['temperature', 'humidity', 'air_quality']:
            stats[col] = {
                'mean': round(df[col].mean(), 2),
                'median': round(df[col].median(), 2),
                'min': round(df[col].min(), 2),
                'max': round(df[col].max(), 2)
            }

        return JsonResponse(stats)
