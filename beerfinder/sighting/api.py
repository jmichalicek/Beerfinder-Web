from django.conf import settings
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

import foursquare

from .models import Sighting
from .serializers import SightingSerializer

class SightingViewSet(viewsets.ModelViewSet):
    queryset = Sighting.objects.all()
    serializer_class = SightingSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def pre_save(self, obj):
        obj.user = self.request.user

    def get_queryset(self):
        queryset = self.queryset

        # I am not settled on this and may switch to url path params for by beer sightings
        # but then need to mess with more advanced routing
        beer_slug = self.request.QUERY_PARAMS.get('beer', None)
        if beer_slug:
            queryset = queryset.filter(beer__slug=beer_slug)

        return queryset

    def get_nearby_sightings(self, request, *args, **kwargs):
        # This implementation using foursquare is not really going to do the trick.
        # This will need implemented storing latitude and longitude for each location
        # which has a sighting locally and then figuring out the closest locally.
        latitude = request.QUERY_PARAMS.get('latitude', None)
        longitude = request.QUERY_PARAMS.get('longitude', None)

        queryset = self.queryset

        client_id = settings.FOURSQUARE_CLIENT_ID
        client_secret = settings.FOURSQUARE_CLIENT_SECRET
        client = foursquare.Foursquare(client_id=client_id, client_secret=client_secret)

        # search category ids
        # 4bf58dd8d48988d17f941735 theaters
        # 4bf58dd8d48988d1e5931735 music venue
        # 4d4b7105d754a06374d81259 food
        # 4d4b7105d754a06376d81259 nightlife spots (bars, breweries included)
        #4bf58dd8d48988d1f9941735 grocery
        # 4d954b0ea243a5684a65b473 convenience stores

        venues = client.venues.explore({'ll': '{0},{1}'.format(latitude, longitude),
                                        'sortByDistance': 1,
                                        'limit': 50,
                                        })


        venue_ids = []
        import itertools
        for group in venues['groups']:
            for item in group['items']:
                print item['venue']
                print '\n\n'
            venue_ids = itertools.chain(venue_ids, (item['venue']['id'] for item in group['items']))

        venue_ids = list(venue_ids)
        print venue_ids

        return Response(queryset.filter(venue__foursquare_id__in=venue_ids))
        #print venues['groups'][0]['items'][3]['venue']['id']
