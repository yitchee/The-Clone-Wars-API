from django.shortcuts import render, HttpResponse
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

import random

from .models import Vehicle
from .serializers import VehicleSerializer

from api.serializers import GenericSerializer
from api.views import BaseRandomView, BaseIdView
from api.utils import validate_request, set_options_response


MODEL = Vehicle


@api_view(['GET', 'OPTIONS'])
def index(request):
    if request.method == 'OPTIONS':
        return set_options_response()

    result = validate_request(request)
    if 'error' in result:
        return Response({"error": result['error']}, status=result['status'], headers=settings.CORS_HEADERS)

    name = request.GET.get('name', None)
    vehicle_class = request.GET.get('class', None)
    affiliation = request.GET.get('affiliation', None)
    manufacturer = request.GET.get('manufacturer', None)
    page = request.GET.get('page', 0)

    vehicles_set = Vehicle.objects.all().order_by('id')
    if name:
        vehicles_set = vehicles_set.filter(name__icontains=name)
    
    if vehicle_class:
        # Avaliable Options : 'Starfighter', 'Freighter', 'Walker', 'Star Destroyer', 
        # 'Unknown', 'Tank', 'Gunship', 'Frigate', 'Transport', 'Cruiser', 'Flagship',
        # 'Shuttle', 'Speeder', 'Capital Ship', 'Battleship', 'Repulsorcraft' ,'Vessel'
        # 'Dreadnaught', 'Carrier'
        vehicles_set = vehicles_set.filter(info__class__icontains=vehicle_class)

    if affiliation:
        vehicles_set = vehicles_set.filter(info__affiliation__icontains=affiliation)

    if manufacturer:
        # 'Rothana Heavy Engineering', 'Kuat Drive Yards', 'Kuat Systems Engineering',
        # 'Hoar Chall Engineering', 'Unknown', 'Umbarans', 'Slayn & Korpil', 'Gallofree Yards',
        # 'Hoersch-Kessel Drive, Inc.', 'Zygerrian Slave Empire', 'Corellian Engineering',
        # 'Quarren', 'MandalMotors', 'Techno Union', 'Baktoid Armor Workshop', 'Botajef Shipyards',
        # 'Lantillian ShipWrights', 'Huppla Pasa Tisc Shipwrights Collective', 'SoroSuub Corporation'
        # 'Cygnus Spaceworks', 'Trade Federation', 'Kalevala Spaceworks'
        vehicles_set = vehicles_set.filter(info__manufacturer__icontains=manufacturer)

    if page:
        try:
            page = int(page)
        except:
            page = 1;
        start = settings.RESOURCE_LIMIT*(page-1)
        end = settings.RESOURCE_LIMIT*(page-1)+settings.RESOURCE_LIMIT
        vehicles_set = vehicles_set[start:end]
    else:
        vehicles_set = vehicles_set[0:settings.RESOURCE_LIMIT]
    
    serializer = VehicleSerializer(vehicles_set, many=True)

    # If nothing matches queries
    if not serializer.data:
        return Response({"error": settings.MSG_404}, status=404, headers=settings.CORS_HEADERS)

    return Response(serializer.data, headers=settings.CORS_HEADERS)


class RandomVehicleView(BaseRandomView):
    model = MODEL


class VehicleIdView(BaseIdView):
    model = MODEL