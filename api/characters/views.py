from django.shortcuts import render, HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

import random

from .models import Character
from .serializers import CharacterSerializer


# Global variables
resource_limit = 50
MSG_404 = "Resources do not exist"


@api_view(['GET'])
def index(request):
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
        characters_set = characters_set[resource_limit*(page-1):resource_limit*(page-1)+resource_limit]
    else:
        characters_set = characters_set[0:resource_limit]
    
    serializer = CharacterSerializer(characters_set, many=True)

    # If nothing matches queries
    if not serializer.data:
        return Response({"error": MSG_404}, status=404)

    return Response(serializer.data)


@api_view(['GET'])
def characters_random(request):
    characters = Character.objects.all()
    random_character = random.choice(characters)
    serializer = CharacterSerializer(random_character, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def characters_id(request, id):
    try:
        characters = Character.objects.get(id=id)
    except:
        return Response({"error": MSG_404}, status=404)
        
    serializer = CharacterSerializer(characters, many=False)
    return Response(serializer.data)