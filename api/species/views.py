from django.shortcuts import render, HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

import random

from .models import Species
from .serializers import SpeciesSerializer


def index(request):
    return HttpResponse('<h1>Species</h1>')


@api_view(['GET'])
def species_random(request):
    species = Species.objects.all()
    random_species = random.choice(species)
    serializer = SpeciesSerializer(random_species, many=False)
    return Response(serializer.data)