"""
URL configuration for SCGSensor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf.urls import url,include
from sensorApp.views import CSVUploadView , GetProcessed , GetAggregated


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sensor/data', CSVUploadView.as_view(), name='upload-csv'),
    path('sensor/processed', GetProcessed.get_processed_sensor_data, name='get_processed_sensor_data'),
    path('sensor/aggregated', GetAggregated.get_aggregated_sensor_data, name='get_aggregated_sensor_data'),
]
