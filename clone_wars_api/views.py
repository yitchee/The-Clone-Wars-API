from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

import random

from api.characters.models import Character
from .serializers import GenericSerializer
from api.characters.serializers import CharacterSerializer
from api.models import ApiKey


class ApiKeyCheckMixin():
    key = ApiKey
    def validate_apikey(self, request):
        try:
            key = request.headers['X-API-KEY']
        except:
            raise(KeyError)

        # Check if API key is valid and within limit
        try:
            key = ApiKey.objects.get(key=key)
            limit = key.daily_limit
            if limit > 0:
                key.daily_limit = limit - 1
            else:
                raise(LimitExceededException)
            key.save()
        except LimitExceededException:
            raise(LimitExceededException)
        except:
            raise(ObjectDoesNotExist)


class BaseRandomView(ApiKeyCheckMixin, APIView):
    serializer = GenericSerializer()
    data_list = []

    def get(self, request):
        # Validate API key
        try:
            self.validate_apikey(request)
        except KeyError:
            return Response({'error': 'Please provide an API key'}, status=401)
        except ObjectDoesNotExist:
            return Response({'error': 'Invalid API key'}, status=401)
        except LimitExceededException:
            return Response({'error': 'Daily limit exceeded.'}, status=429)

        random_object = random.choice(self.data_list)
        self.serializer = GenericSerializer(random_object, many=False)
        return Response(self.serializer.data)


class BaseIdView(ApiKeyCheckMixin, APIView):
    model = object
    serializer = GenericSerializer()
    data = {}

    def get(self, request, id):
        # Validate API key
        try:
            self.validate_apikey(request)
        except KeyError:
            return Response({'error': 'Please provide an API key'}, status=401)
        except ObjectDoesNotExist:
            return Response({'error': 'Invalid API key'}, status=401)
        except LimitExceededException:
            return Response({'error': 'Daily limit exceeded.'}, status=429)

        try:
            data = self.model.objects.get(id=id)
        except:
            return Response({"error": settings.MSG_404}, status=404)
        
        serializer = GenericSerializer(data, many=False)
        return Response(serializer.data)


class LimitExceededException(Exception):
    pass