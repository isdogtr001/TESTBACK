from django.conf.urls import url
from sensorApp import views

from django.conf.urls.static import static
# from django.conf import settings

urlpatterns=[
    url(r'^sensors$',views.sensorsApi),
    url(r'^sensors/([0-9]+)$',views.sensorsApi),
 
]