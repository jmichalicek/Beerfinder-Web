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
from core.permissions import IsOwnerOrReadOnlyPermissions
from venue.models import Venue

from .forms import SightingModelForm, SightingImageForm
from .models import Sighting, SightingConfirmation, SightingImage
from .serializers import (SightingSerializer, SightingConfirmationSerializer,
                          PaginatedSightingCommentSerializer, SightingCommentSerializer,
                          PaginatedDistanceSightingSerializer, DistanceSightingSerializer,
                          SightingImageSerializer, PaginatedSightingSerializer,
                          PaginatedSightingImageSerializer)


class SightingViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    """
    ViewSet to list and create sightings.
    """
    queryset = Sighting.objects.select_related('user', 'beer', 'beer__brewery', 'venue').all()
    serializer_class = SightingSerializer
    pagination_serializer_class = PaginatedSightingSerializer
    paginator = InfinitePaginator
    permission_classes = (IsOwnerOrReadOnlyPermissions, )
    paginate_by = 25
    paginate_by_param = 'page_size'

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

    @detail_route(methods=['POST'])
    def confirm_available(self, request, *args, **kwargs):
        """
        Mark a sighting as still available

        TODO: REMOVE
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

        TODO: REMOVE
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


class SightingImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for :class:`sighting.models.SightingImage`
    """

    queryset = SightingImage.objects.all()
    serializer_class = SightingImageSerializer
    paginator = InfinitePaginator
    pagination_serializer_class = PaginatedSightingImageSerializer
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
    queryset = SightingComment.objects.select_related('user', 'sighting').all()
    serializer_class = SightingCommentSerializer
    pagination_serializer_class = PaginatedSightingCommentSerializer
    paginator = InfinitePaginator
    permission_classes = (IsOwnerOrReadOnlyPermissions, )
    paginate_by = 100
    paginate_by_param = 'page_size'

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
