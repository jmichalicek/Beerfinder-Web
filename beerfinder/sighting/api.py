from django.conf import settings
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action

import foursquare

from beer.models import Beer
from venue.models import Venue

from .forms import SightingModelForm
from .models import Sighting, SightingConfirmation
from .serializers import SightingSerializer, SightingConfirmationSerializer

class SightingViewSet(viewsets.ModelViewSet):
    queryset = Sighting.objects.select_related('user', 'beer', 'beer__brewery', 'location').all()
    serializer_class = SightingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    paginate_by = 25
    paginate_by_param = 'page_size'

    def create(self, request, *args, **kwargs):
        """
        Does a whole bunch of extra special stuff
        """

        try:
            beer = Beer.objects.get(slug=request.DATA.get('beer'))
        except Beer.DoesNotExist:
            return Response({'error': 'Beer does not exist'}, status=400)

        foursquare_id = request.DATA.get('foursquare_venue_id')
        try:
            venue = Venue.objects.get(foursquare_id=foursquare_id)
        except Venue.DoesNotExist:
            venue = Venue.retrieve_from_foursquare(foursquare_id)
            venue.save()

        form_data = {'beer': beer.id, 'venue': venue.id, 'user': request.user.id, 'comment': request.DATA.get('comment', '')}

        sighting_form = SightingModelForm(form_data, request.FILES)
        # This should be doable using the serializer as the form, but I'm missing something
        # sighting_form = self.get_serializer(data=form_data, files=request.FILES)
        if sighting_form.is_valid():
            sighting = sighting_form.save()
            serialized = SightingSerializer(sighting)
            return Response(serialized.data, status=201) #201, created
        else:
            return Response({'form_errors': sighting_form.errors}, status=400)

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
            venue_ids = itertools.chain(venue_ids, (item['venue']['id'] for item in group['items']))

        venue_ids = list(venue_ids)

        #queryset = queryset.filter(venue__foursquare_id__in=venue_ids)
        response_data = SightingSerializer(queryset)
        return Response(response_data.data)
        #print venues['groups'][0]['items'][3]['venue']['id']

    @action(methods=['POST'])
    def confirm_available(self, request, *args, **kwargs):
        """
        Mark a sighting as still available
        """
        sighting = self.get_object()
        confirmation_serializer = SightingConfirmationSerializer(data={'sighting': sighting.pk, 'user': request.user.pk, 'is_available': True})
        if confirmation_serializer.is_valid():
            confirmation = confirmation_serializer.save()
            return Response(SightingSerializer(sighting).data, status=201)
        else:
            print confirmation_serializer.errors
            # should return a more generic error here
            return Response(confirmation_serializer.errors, status=400)

    @action(methods=['POST'])
    def confirm_unavailable(self, request, *args, **kwargs):
        """
        Mark a sighting as no longer available
        """
        sighting = self.get_object()
        confirmation_serializer = SightingConfirmationSerializer(data={'sighting': sighting.pk, 'user': request.user.pk, 'is_available': False})
        if confirmation_serializer.is_valid():
            confirmation = confirmation_serializer.save()
            return Response(SightingSerializer(sighting).data, status=201)
        else:
            print confirmation_serializer.errors
            # should return a more generic error here
            return Response(confirmation_serializer.errors, status=400)
