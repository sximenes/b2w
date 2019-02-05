from django.shortcuts import render
from dynamic_rest.viewsets import DynamicModelViewSet

from sw.models import Planet
from sw.serializers import PlanetSerializer

# Create your views here.
class PlanetViewSet(DynamicModelViewSet):
    serializer_class = PlanetSerializer
    queryset = Planet.objects.all()