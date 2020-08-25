from django.views import View

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

import random

from .serializers import GenericSerializer
from api.characters.serializers import CharacterSerializer


class BaseRandomView(APIView):
    serializer = GenericSerializer()
    data_list = []

    def get(self, request):
        random_object = random.choice(self.data_list)
        self.serializer = GenericSerializer(random_object, many=False)
        return Response(self.serializer.data)
