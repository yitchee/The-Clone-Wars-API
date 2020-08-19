from django.shortcuts import render, HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

import random

from .models import Planet
from .serializers import PlanetSerializer


def index(request):
    return HttpResponse('<h1>Planets</h1>')


@api_view(['GET'])
def planets_random(request):
    planets = Planet.objects.all()
    random_planets = random.choice(planets)
    serializer = PlanetSerializer(random_planets, many=False)
    return Response(serializer.data)