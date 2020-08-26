from django.shortcuts import render, HttpResponse
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

import random

from .models import Planet
from .serializers import PlanetSerializer

from clone_wars_api.serializers import GenericSerializer
from clone_wars_api.views import BaseRandomView, BaseIdView


@api_view(['GET'])
def index(request):
    name = request.GET.get('name', None)
    affiliation = request.GET.get('affiliation', None)
    region = request.GET.get('region', None)
    page = int(request.GET.get('page', 0))

    planets_set = Planet.objects.all().order_by('id')

    if name:
        planets_set = planets_set.filter(name__icontains=name)
    
    if affiliation:
        planets_set = planets_set.filter(info__affiliation__icontains=affiliation)

    if region:
        planets_set = planets_set.filter(info__region__icontains=region)

    if page:
        start = settings.RESOURCE_LIMIT*(page-1)
        end = settings.RESOURCE_LIMIT*(page-1)+settings.RESOURCE_LIMIT
        planets_set = planets_set[start:end]
    else:
        planets_set = planets_set[0:settings.RESOURCE_LIMIT]

    serializer = PlanetSerializer(planets_set, many=True)

    # If nothing matches queries
    if not serializer.data:
        return Response({"error": settings.MSG_404}, status=404)

    return Response(serializer.data)


class RandomPlanetView(BaseRandomView):
    data_list = Planet.objects.all()
    serializer = GenericSerializer
    serializer.Meta.model = Planet


class PlanetIdView(BaseIdView):
    model = Planet
    serializer = GenericSerializer
    serializer.Meta.model = model