from django.shortcuts import render, HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

import random

from .models import Character
from .serializers import CharacterSerializer


def index(request):
    return HttpResponse('<h1>Characters</h1>')


@api_view(['GET'])
def characters_random(request):
    characters = Character.objects.all()
    random_character = random.choice(characters)
    serializer = CharacterSerializer(random_character, many=False)
    return Response(serializer.data)