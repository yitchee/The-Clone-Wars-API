from django.shortcuts import render, HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

import random

from .models import Vehicle
from .serializers import VehicleSerializer


def index(request):
    return HttpResponse('<h1>Vehicles</h1>')


@api_view(['GET'])
def vehicles_random(request):
    vehicles = Vehicle.objects.all()
    random_vehicle = random.choice(vehicles)
    serializer = VehicleSerializer(random_vehicle, many=False)
    return Response(serializer.data)