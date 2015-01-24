from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.gis.geos import Point, fromstr, GEOSGeometry
from django.db import transaction

from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework_extensions.key_constructor.constructors import DefaultListKeyConstructor

import foursquare

from beer.models import Beer
from core.paginator import InfinitePaginator, InfinitePage
from core.cache_keys import DefaultPaginatedListKeyConstructor
from venue.models import Venue

from .forms import SightingModelForm, SightingImageForm
from .models import Sighting, SightingConfirmation
from .serializers import (SightingSerializer, SightingConfirmationSerializer,
                          PaginatedSightingCommentSerializer, SightingCommentSerializer,
                          PaginatedDistanceSightingSerializer, DistanceSightingSerializer,
                          SightingImageSerializer, PaginatedSightingSerializer)


class SightingViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    queryset = Sighting.objects.select_related('user', 'beer', 'beer__brewery', 'venue').all()
    serializer_class = SightingSerializer
    pagination_serializer_class = PaginatedSightingSerializer
    paginator = InfinitePaginator
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

        form_data = {'beer': beer.id, 'venue': venue.id, 'user': request.user.id,
                     'comment': request.DATA.get('comment', ''),
                     'serving_types': request.DATA.getlist('serving_types', [])}

        transaction.set_autocommit(False)
        try:
            sighting_form = SightingModelForm(form_data)
            # This should be doable using the serializer as the form, but I'm missing something
            # sighting_form = self.get_serializer(data=form_data, files=request.FILES)
            if sighting_form.is_valid():
                sighting = sighting_form.save()
            else:
                transaction.rollback()
                return Response({'form_errors': sighting_form.errors}, status=400)

            if request.FILES:
                # muck with the files dict because we receive the image in a param called 'image'
                # but the form needs it to be named 'original'
                file_dict = {'original': request.FILES.get('image')}
                image_form = SightingImageForm({'sighting': sighting.id, 'user': request.user.id}, file_dict)
                if image_form.is_valid():
                    image = image_form.save()
                    transaction.commit()

                    # commit before generate_images in case of imagekit async backend
                    try:
                        image.generate_images()
                    except Exception, e:
                        transaction.rollback()
                        raise
                    else:
                        # extra commit here in case imagekit backend is not async
                        # or CELERY_ALWAYS_EAGER=True so that the updated model will be saved
                        transaction.commit()
                else:
                    transaction.rollback()
                    return Response({'form_errors': image_form.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # no files to try to save, just commit the sighting
                transaction.commit()
        finally:
            transaction.set_autocommit(True)

        serialized = self.get_serializer(sighting)
        return Response(serialized.data, status=201)

    def pre_save(self, obj):
        obj.user = self.request.user

    def get_queryset(self, prefetch=True):
        queryset = self.queryset

        # I am not settled on this and may switch to url path params for by beer sightings
        # but then need to mess with more advanced routing
        beer_slug = self.request.QUERY_PARAMS.get('beer', None)

        if beer_slug:
            queryset = queryset.filter(beer__slug=beer_slug)

        if prefetch:
            queryset = queryset.prefetch_related('sighting_images', 'serving_types')
        return queryset

    @detail_route(methods=['POST'])
    def confirm_available(self, request, *args, **kwargs):
        """
        Mark a sighting as still available
        """
        sighting = self.get_object()
        confirmation_serializer = SightingConfirmationSerializer(data={'sighting': sighting.pk, 'user': request.user.pk, 'is_available': True}, context={'request': request})
        if confirmation_serializer.is_valid():
            confirmation = confirmation_serializer.save()
            return Response(self.get_serializer(sighting).data, status=201)
        else:
            # should return a more generic error here
            return Response(confirmation_serializer.errors, status=400)

    @detail_route(methods=['post'])
    def confirm_unavailable(self, request, *args, **kwargs):
        """
        Mark a sighting as no longer available
        """
        sighting = self.get_object()
        serializer_context = {'request': request}
        confirmation_serializer = SightingConfirmationSerializer(data={'sighting': sighting.pk, 'user': request.user.pk, 'is_available': False}, context=serializer_context)
        if confirmation_serializer.is_valid():
            confirmation = confirmation_serializer.save()
            return Response(self.get_serializer(sighting).data, status=201)
        else:
            # should return a more generic error here
            return Response(confirmation_serializer.errors, status=400)

    @detail_route(methods=['post'])
    def add_comment(self, request, *args, **kwargs):
        """
        TODO: Remove this and just use a comment resource!
        """
        sighting = self.get_object()
        serializer_context = {'request': request}
        serializer = SightingCommentSerializer(data=request.POST, context=serializer_context)
        if serializer.is_valid():
            serializer.object.user = request.user
            serializer.object.sighting = sighting
            comment = serializer.save()
            return Response(serializer.data, status=201)

        else:
            return Response(serializer.errors, status=400)

    @detail_route(methods=['get'])
    @cache_response(10, key_func=DefaultPaginatedListKeyConstructor())
    def comments(self, request, *args, **kwargs):
        """
        Get the comments for a sighting

        TODO: Remove this and use a comments resource
        """
        sighting = self.get_object()
        queryset = sighting.comments.all()
        paginator = InfinitePaginator(queryset, 10)

        page = request.QUERY_PARAMS.get('page')
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(1)

        serializer_context = {'request': request}
        serializer = PaginatedSightingCommentSerializer(comments,
                                                        context=serializer_context)

        return Response(serializer.data)


class NearbySightingAPIView(generics.ListAPIView):
    """
    View to list :class:`beer.models.ServingType`
    """

    queryset = Sighting.objects.all()
    serializer_class = DistanceSightingSerializer
    pagination_serializer_class = PaginatedDistanceSightingSerializer
    paginator = InfinitePaginator
    paginate_by = 50
    paginate_by_param = 'page_size'

    def get_queryset(self):
        # implementing search here, but may move to its own endpoint
        # with django haystack implementing proper full text search

        request = self.request
        queryset = super(NearbySightingAPIView, self).get_queryset()
        beer_slug = self.request.QUERY_PARAMS.get('beer', None)

        if beer_slug:
            queryset = queryset.filter(beer__slug=beer_slug)

        latitude = request.QUERY_PARAMS.get('latitude', None)
        longitude = request.QUERY_PARAMS.get('longitude', None)
        origin = Point(float(longitude), float(latitude))

        queryset = queryset.distance(origin, field_name='venue__point').order_by('distance')
        queryset = queryset.prefetch_related('sighting_images', 'serving_types')

        return queryset

    # this cache will end up more or less per user due to location awareness
    @cache_response(60 * 5, key_func=DefaultListKeyConstructor())
    def get(self, request, *args, **kwargs):
        """
        Return a list of sightings sorted by distance from the point specified.
        """
        return super(NearbySightingAPIView, self).get(request, *args, **kwargs)


class SightingImageViewset(viewsets.ModelViewSet):
    # TODO: Make this just use CreateModelMixin and whatever it depends on until/if
    # supporting other methods is desired?
    serializer_class = SightingImageSerializer

    def pre_save(self, obj):
        obj.user = self.request.user
    
    def create(self, *args, **kwargs):
        """
        Create a SightingImage.  Ensures that the sighting was created by the user
        and will only allow 1 image upload.
        """
        pass
