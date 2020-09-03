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
from api.utils import validate_request, set_options_response


CORS_HEADERS = settings.CORS_HEADERS
MSG_404 = "Resources do not exist"


def index(request):
    return render(request, 'api/index.html')


class ApiKeyCheckMixin():
    key = ApiKey
    def validate_request(self, request):
        return validate_request(request)


class BaseRandomView(ApiKeyCheckMixin, APIView):
    model = object
    Serializer = GenericSerializer

    def get(self, request):
        response = Response()
        response.headers = CORS_HEADERS

        result = self.validate_request(request)
        if 'error' in result:
            return Response({"error": result['error']}, status=result['status'], headers=CORS_HEADERS)
        data_list = self.model.objects.all()
        random_object = random.choice(data_list)
        self.Serializer.Meta.model = self.model
        serializer = self.Serializer(random_object, many=False)
        return Response(serializer.data, headers=CORS_HEADERS)

    def options(self, request):
        print(123)
        response = set_options_response()
        return response


class BaseIdView(ApiKeyCheckMixin, APIView):
    model = object
    Serializer = GenericSerializer

    def get(self, request, id):
        self.Serializer.Meta.model = self.model
        
        result = self.validate_request(request)
        if 'error' in result:
            return Response({"error": result['error']}, status=result['status'], headers=CORS_HEADERS)

        try:
            data = self.model.objects.get(id=id)
        except:
            return Response({"error": MSG_404}, status=404)

        serializer = self.Serializer(data, many=False)
        return Response(serializer.data, headers=CORS_HEADERS)

    # Handle 'OPTIONS' request | tells browser that CORS is enabled
    def options(self, request, id):
        response = set_options_response()
        return response