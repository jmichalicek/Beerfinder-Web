from django.conf import settings
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

import foursquare

from .models import Sighting
from .serializers import VenueSerializer

class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = SightingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
