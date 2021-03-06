from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.gis.geos import Point, fromstr, GEOSGeometry
from django.db import transaction

from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.cache.mixins import CacheResponseMixin

import foursquare

from beer.models import Beer
from core.cache_keys import QueryParamsKeyConstructor
from core.permissions import IsOwnerOrReadOnlyPermissions
from core.viewsets import CreateListRetrieveViewSet
from venue.models import Venue
from core.cache_keys import QueryParamsKeyConstructor

from .forms import SightingModelForm, SightingImageForm
from .models import Sighting, SightingConfirmation, SightingImage, Comment
from .serializers import (SightingSerializer, SightingConfirmationSerializer,
                          SightingCommentSerializer, DistanceSightingSerializer,
                          SightingImageSerializer)


class SightingViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    """
    ViewSet to list and create sightings.
    """
    queryset = Sighting.objects.select_related('user', 'beer', 'beer__brewery', 'venue').all()
    serializer_class = SightingSerializer
    permission_classes = (IsOwnerOrReadOnlyPermissions, )
    page_size = 25
    paginate_by_param = 'page_size'
    list_cache_key_func = QueryParamsKeyConstructor()

    def perform_create(self, serializer):
        """
        Ensures that the user is set on the saved sighting.
        This could also be moved to living on the serializer
        """
        serializer.save(user=self.request.user)

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


class NearbySightingAPIView(generics.ListAPIView):
    """
    View to list :class:`beer.models.ServingType`
    """

    queryset = Sighting.objects.all()
    serializer_class = DistanceSightingSerializer

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
    @cache_response(60 * 5, key_func=QueryParamsKeyConstructor())
    def get(self, request, *args, **kwargs):
        """
        Return a list of sightings sorted by distance from the point specified.
        """
        return super(NearbySightingAPIView, self).get(request, *args, **kwargs)


class SightingImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for :class:`sighting.models.SightingImage`
    """

    queryset = SightingImage.objects.all()
    serializer_class = SightingImageSerializer
    page_size = 50
    permission_classes = (IsOwnerOrReadOnlyPermissions, )

    def get_queryset(self):
        # Filter by username/email instead of by user id?
        sighting = self.request.QUERY_PARAMS.get('sighting', None)
        user = self.request.QUERY_PARAMS.get('user', None)

        queryset = super(SightingImageViewSet, self).get_queryset()

        if sighting:
            queryset = queryset.filter(sighting_id=sighting)

        if user:
            queryset = queryset.filter(user_id=user)

        return queryset

    def perform_create(self, serializer):
        """
        Calls serializer.save() to create the image and then
        generates the different image sizes
        """
        image = serializer.save()
        image.generate_images()


class SightingCommentViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    """
    ViewSet to list and create sightings.
    """
    # TODO: Really no need for edit or delete functionality currently.
    # Perhaps this should be a Create/Retrieve/List view?

    # TODO: Override paginator to account for custom page size... maybe
    queryset = Comment.objects.select_related('user', 'sighting').all()
    serializer_class = SightingCommentSerializer
    permission_classes = (IsOwnerOrReadOnlyPermissions, )
    list_cache_key_func = QueryParamsKeyConstructor()
    cache_timeout = 2

    def get_queryset(self):
        # filter by username/email instead of user id?
        sighting = self.request.QUERY_PARAMS.get('sighting', None)
        user = self.request.QUERY_PARAMS.get('user', None)

        queryset = super(SightingCommentViewSet, self).get_queryset()

        if sighting:
            queryset = queryset.filter(sighting_id=sighting)

        if user:
            queryset = queryset.filter(user_id=user)

        return queryset

    def perform_create(self, serializer):
        """
        Ensures that the user is set on the saved comment.
        This could also be moved to living on the serializer
        """
        serializer.save(user=self.request.user)

    # override the caching here because CacheResponseMixin does not
    # seem to allow configuring the timeout
    @cache_response(10, key_func=QueryParamsKeyConstructor())
    def list(self, request, *args, **kwargs):
        return super(SightingCommentViewSet, self).list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Not allowing update for now, return HTTP 405
        """
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        """
        Not allowing delete for now, return HTTP 405
        """
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SightingConfirmationAPIView(generics.CreateAPIView):
    permissions = (permissions.IsAuthenticatedOrReadOnly, )
    queryset = SightingConfirmation.objects.all()
    serializer_class = SightingConfirmationSerializer
