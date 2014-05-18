from django.conf import settings
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import link

from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor
from rest_framework_extensions.key_constructor.bits import (
    KeyBitBase,
    RetrieveSqlQueryKeyBit,
    ListSqlQueryKeyBit,
    PaginationKeyBit,
    UserKeyBit,
    QueryParamsKeyBit
)

import foursquare

from .models import Venue
from .serializers import VenueSerializer

class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


# Is there some way that the lat and lon could be generalized a bit so
# that they could be used as part of the cache key instead of user
class FoursquareVenueListKeyConstructor(DefaultKeyConstructor):
    user = UserKeyBit()
    offset  = QueryParamsKeyBit(
        ['offset',]
    )

class FoursquareSearchListKeyConstructor(DefaultKeyConstructor):
    user = UserKeyBit()
    offset_and_search = QueryParamsKeyBit(
        ['query', ])

class FoursquareVenueViewSet(viewsets.ViewSet):
    """
    A ViewSet to work as a passthrough for communicating with Foursquare's Venue API
    while not worrying about any local models.
    """

    @cache_response(60 * 3, key_func=FoursquareVenueListKeyConstructor())
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

    @cache_response(60 * 3, key_func=FoursquareSearchListKeyConstructor())
    def search(self, request):
        """
        User the Foursquare venue search endpoint and return the results
        """

        latitude = request.QUERY_PARAMS.get('latitude', None)
        longitude = request.QUERY_PARAMS.get('longitude', None)
        query = request.QUERY_PARAMS.get('query', '')

        client_id = settings.FOURSQUARE_CLIENT_ID
        client_secret = settings.FOURSQUARE_CLIENT_SECRET
        client = foursquare.Foursquare(client_id=client_id, client_secret=client_secret)

        venues = client.venues.search({'ll': '{0},{1}'.format(latitude, longitude),
                                       'radius': 3000,
                                       'limit': 50,
                                       'query': query,
                                       'intent': 'browse',
                                       })
        return Response(venues)

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
