from django.shortcuts import render, HttpResponse
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

import random

from .models import Species
from .serializers import SpeciesSerializer

from api.serializers import GenericSerializer
from api.views import BaseRandomView, BaseIdView
from api.utils import validate_request, set_options_response


MODEL = Species


@api_view(['GET', 'OPTIONS'])
def index(request):
    if request.method == 'OPTIONS':
        return set_options_response()

    result = validate_request(request)
    if 'error' in result:
        return Response({"error": result['error']}, status=result['status'], headers=settings.CORS_HEADERS)

    name = request.GET.get('name', None)
    designation = request.GET.get('designation', None)
    homeworld = request.GET.get('homeworld', None)
    page = int(request.GET.get('page', 0))

    species_set = Species.objects.all().order_by('id')
    if name:
        species_set = species_set.filter(name__icontains=name)
    
    if designation:
        # Avaliable Options : 'Sentient', 'Non-Sentient', 'Semi-Sentient', 'Undefined'
        species_set = species_set.filter(info__designation__iexact=designation)

    if homeworld:
        # Avaliable Options : 'Sentient', 'Non-Sentient', 'Semi-Sentient', 'Undefined'
        species_set = species_set.filter(info__homeworld__icontains=homeworld)

    if page:
        start = settings.RESOURCE_LIMIT*(page-1)
        end = settings.RESOURCE_LIMIT*(page-1)+settings.RESOURCE_LIMIT
        species_set = species_set[start:end]
    else:
        species_set = species_set[0:settings.RESOURCE_LIMIT]
    
    serializer = SpeciesSerializer(species_set, many=True)

    # If nothing matches queries
    if not serializer.data:
        return Response({"error": settings.MSG_404}, status=404, headers=settings.CORS_HEADERS)
    
    return Response(serializer.data, headers=settings.CORS_HEADERS)


class RandomSpeciesView(BaseRandomView):
    model = MODEL


class SpeciesIdView(BaseIdView):
    model = MODEL