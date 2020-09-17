from django.shortcuts import render, HttpResponse
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

import random

from .models import Character
from .serializers import CharacterSerializer

from api.serializers import GenericSerializer
from api.views import BaseRandomView, BaseIdView
from api.utils import validate_request, set_options_response


MODEL = Character


@api_view(['GET', 'OPTIONS'])
def index(request):
    if request.method == 'OPTIONS':
        return set_options_response()

    result = validate_request(request)
    if 'error' in result:
        return Response({"error": result['error']}, status=result['status'], headers=settings.CORS_HEADERS)
    
    name = request.GET.get('name', None)
    species = request.GET.get('species', None)
    gender = request.GET.get('gender', None)
    occupation = request.GET.get('occupation', None)
    affiliation = request.GET.get('affiliation', None)
    page = request.GET.get('page', 0)

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
        try:
            page = int(page)
        except:
            page = 1;
        start = settings.RESOURCE_LIMIT*(page-1)
        end = settings.RESOURCE_LIMIT*(page-1)+settings.RESOURCE_LIMIT
        characters_set = characters_set[start:end]
    else:
        characters_set = characters_set[0:settings.RESOURCE_LIMIT]
    
    serializer = CharacterSerializer(characters_set, many=True)

    # If nothing matches queries
    if not serializer.data:
        return Response({"error": settings.MSG_404}, status=404, headers=settings.CORS_HEADERS)

    return Response(serializer.data, headers=settings.CORS_HEADERS)


class RandomCharacterView(BaseRandomView):
    model = MODEL


class CharacterIdView(BaseIdView):
    model = MODEL