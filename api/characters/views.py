from django.shortcuts import render, HttpResponse
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

import random

from .models import Character
from .serializers import CharacterSerializer

from api.serializers import GenericSerializer
from api.views import BaseRandomView, BaseIdView


MODEL = Character


@api_view(['GET'])
def index(request):
    # print(request.headers['X-API-KEY'])
    name = request.GET.get('name', None)
    species = request.GET.get('species', None)
    gender = request.GET.get('gender', None)
    occupation = request.GET.get('occupation', None)
    affiliation = request.GET.get('affiliation', None)
    page = int(request.GET.get('page', 0))

    characters_set = Character.objects.all().order_by('id')
    if name:
        characters_set = characters_set.filter(name__icontains=name)

    if species:
        characters_set = characters_set.filter(info__species__icontains=species)

    if gender:
        characters_set = characters_set.filter(info__gender__icontains=gender)
    
    if occupation:
        characters_set = characters_set.filter(info__occupation_rank__icontains=occupation)
    
    if affiliation:
        characters_set = characters_set.filter(info__affiliation__icontains=affiliation)

    if page:
        start = settings.RESOURCE_LIMIT*(page-1)
        end = settings.RESOURCE_LIMIT*(page-1)+settings.RESOURCE_LIMIT
        characters_set = characters_set[start:end]
    else:
        characters_set = characters_set[0:settings.RESOURCE_LIMIT]
    
    serializer = CharacterSerializer(characters_set, many=True)

    # If nothing matches queries
    if not serializer.data:
        return Response({"error": settings.MSG_404}, status=404)

    return Response(serializer.data)


class RandomCharacterView(BaseRandomView):
    model = MODEL


class CharacterIdView(BaseIdView):
    model = MODEL