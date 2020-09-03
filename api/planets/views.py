from django.shortcuts import render, HttpResponse
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

import random

from .models import Planet
from .serializers import PlanetSerializer

from api.serializers import GenericSerializer
from api.views import BaseRandomView, BaseIdView
from api.utils import validate_request, set_options_response


MODEL = Planet


@api_view(['GET', 'OPTIONS'])
def index(request):
    if request.method == 'OPTIONS':
        return set_options_response()

    result = validate_request(request)
    if 'error' in result:
        return Response({"error": result['error']}, status=result['status'], headers=settings.CORS_HEADERS)

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
        return Response({"error": settings.MSG_404}, status=404, headers=settings.CORS_HEADERS)

    return Response(serializer.data, headers=settings.CORS_HEADERS)


class RandomPlanetView(BaseRandomView):
    model = MODEL


class PlanetIdView(BaseIdView):
    model = MODEL