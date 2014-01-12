from django.conf import settings
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

import foursquare

from .models import Venue
from .serializers import VenueSerializer

class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class FoursquareVenueViewSet(viewsets.ViewSet):
    """
    A ViewSet to work as a passthrough for communicating with Foursquare's Venue API
    while not worrying about any local models.
    """

    def list(self, request):
        """
        Uses foursquare venue explore to get nearby venues
        """
        latitude = request.QUERY_PARAMS.get('latitude', None)
        longitude = request.QUERY_PARAMS.get('longitude', None)
        offset = request.QUERY_PARAMS.get('offset', 0)

        client_id = settings.FOURSQUARE_CLIENT_ID
        client_secret = settings.FOURSQUARE_CLIENT_SECRET
        client = foursquare.Foursquare(client_id=client_id, client_secret=client_secret)

        venues = client.venues.explore({'ll': '{0},{1}'.format(latitude, longitude),
                                        'sortByDistance': 1,
                                        'limit': 50,
                                        'offset': offset,
                                        })

        return Response(venues)

    def search(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
