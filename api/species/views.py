from django.shortcuts import render, HttpResponse
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

import random

from .models import Species
from .serializers import SpeciesSerializer

from api.serializers import GenericSerializer
from api.views import BaseRandomView, BaseIdView


MODEL = Species


@api_view(['GET'])
def index(request):
    name = request.GET.get('name', None)
    designation = request.GET.get('designation', None)
    page = int(request.GET.get('page', 0))

    species_set = Species.objects.all().order_by('id')
    if name:
        species_set = species_set.filter(name__icontains=name)
    
    if designation:
        # Avaliable Options : 'Sentient', 'Non-Sentient', 'Semi-Sentient', 'Undefined'
        species_set = species_set.filter(info__designation__iexact=designation)

    if page:
        start = settings.RESOURCE_LIMIT*(page-1)
        end = settings.RESOURCE_LIMIT*(page-1)+settings.RESOURCE_LIMIT
        species_set = species_set[start:end]
    else:
        species_set = species_set[0:settings.RESOURCE_LIMIT]
    
    serializer = SpeciesSerializer(species_set, many=True)

    # If nothing matches queries
    if not serializer.data:
        return Response({"error": settings.MSG_404}, status=404)
    
    return Response(serializer.data)


class RandomSpeciesView(BaseRandomView):
    model = MODEL


class SpeciesIdView(BaseIdView):
    model = MODEL