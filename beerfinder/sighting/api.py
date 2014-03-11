from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.gis.geos import Point, fromstr, GEOSGeometry

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action, link

import foursquare

from beer.models import Beer
from venue.models import Venue

from .forms import SightingModelForm
from .models import Sighting, SightingConfirmation
from .serializers import (SightingSerializer, SightingConfirmationSerializer,
                          PaginatedSightingCommentSerializer, SightingCommentSerializer,
                          PaginatedDistanceSightingSerializer, DistanceSightingSerializer)

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

        # Spot.objects.filter(point__distance_lte=(origin, D(m=distance_m))).distance(origin).order_by('distance')[:1][0]
        #origin = fromstr("Point({0} {1})".format(longitude, latitude))
        origin = Point(float(longitude), float(latitude))
        queryset = self.queryset.distance(origin, field_name='venue__point').order_by('distance')

        paginator = Paginator(queryset, 25)
        page_number = request.QUERY_PARAMS.get('page')
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        serializer_context = {'request': request}
        serialized = PaginatedDistanceSightingSerializer(page,
                                                         context=serializer_context)
        return Response(serialized.data)

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

    @action(methods=['post'])
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
            # should return a more generic error here
            return Response(confirmation_serializer.errors, status=400)

    @action(methods=['post'])
    def add_comment(self, request, *args, **kwargs):
        sighting = self.get_object()
        serializer = SightingCommentSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.object.user = request.user
            serializer.object.sighting = sighting
            comment = serializer.save()
            return Response(serializer.data, status=201)

        else:
            return Response(serializer.errors, status=400)

    @link()
    def comments(self, request, *args, **kwargs):
        """
        Get the comments for a sighting
        """
        sighting = self.get_object()
        queryset = sighting.comments.all()
        paginator = Paginator(queryset, 10)

        page = request.QUERY_PARAMS.get('page')
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        serializer_context = {'request': request}
        serializer = PaginatedSightingCommentSerializer(comments,
                                                        context=serializer_context)

        return Response(serializer.data)
