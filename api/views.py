from django.shortcuts import render, HttpResponse
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


CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS, HEAD'
}
MSG_404 = "Resources do not exist"


def index(request):
    return render(request, 'api/index.html')


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
    model = object
    Serializer = GenericSerializer

    def get(self, request):
        response = Response()
        response.headers = CORS_HEADERS

        # Check if request is coming from the same origin (for demoing the api in docs)
        print(request.headers)
        # print(request.META)
        try:
            origin = request.META['HTTP_ORIGIN']
        except:
            origin = ''
            
        if settings.DOMAIN_NAME not in origin:
            # Validate API key
            try:
                self.validate_apikey(request)
            except KeyError:
                return Response({'error': 'Please provide an API key'}, status=401, headers=CORS_HEADERS)
            except ObjectDoesNotExist:
                return Response({'error': 'Invalid API key'}, status=401, headers=CORS_HEADERS)
            except LimitExceededException:
                return Response({'error': 'Daily limit exceeded.'}, status=429, headers=CORS_HEADERS)
        
        data_list = self.model.objects.all()
        random_object = random.choice(data_list)
        self.Serializer.Meta.model = self.model
        serializer = self.Serializer(random_object, many=False)
        return Response(serializer.data, headers=CORS_HEADERS)

    def options(self, request):
        response = setResponseForOptionsRequest()
        return response


class BaseIdView(ApiKeyCheckMixin, APIView):
    model = object
    Serializer = GenericSerializer

    def get(self, request, id):
        self.Serializer.Meta.model = self.model
        
        # Check if request is coming from the same origin (for demoing the api in docs)
        if settings.DOMAIN_NAME not in request.headers['Origin']:
            # Validate API key
            try:
                self.validate_apikey(request)
            except KeyError:
                return Response({'error': 'Please provide an API key'}, status=401, headers=CORS_HEADERS)
            except ObjectDoesNotExist:
                return Response({'error': 'Invalid API key'}, status=401, headers=CORS_HEADERS)
            except LimitExceededException:
                return Response({'error': 'Daily limit exceeded.'}, status=429, headers=CORS_HEADERS)

        try:
            data = self.model.objects.get(id=id)
        except:
            return Response({"error": MSG_404}, status=404)

        serializer = self.Serializer(data, many=False)
        return Response(serializer.data, headers=CORS_HEADERS)

    # Handle 'OPTIONS' request | tells browser that CORS is enabled
    def options(self, request, id):
        response = setResponseForOptionsRequest()
        return response


class LimitExceededException(Exception):
    pass


def setResponseForOptionsRequest():
    response = Response()
    response['Allow'] = 'GET, OPTIONS, HEAD'
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'x-api-key'
    return response