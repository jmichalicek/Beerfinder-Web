from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.gis.geos import Point, fromstr, GEOSGeometry
from django.db import transaction

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action, link

from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.cache.mixins import CacheResponseMixin
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

from beer.models import Beer
from core.paginator import InfinitePaginator, InfinitePage
from core.cache_keys import DefaultPaginatedListKeyConstructor
from venue.models import Venue

from .forms import SightingModelForm, SightingImageForm
from .models import Sighting, SightingConfirmation
from .serializers import (SightingSerializer, SightingConfirmationSerializer,
                          PaginatedSightingCommentSerializer, SightingCommentSerializer,
                          PaginatedDistanceSightingSerializer, DistanceSightingSerializer,
                          SightingImageSerializer)


class SightingViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    queryset = Sighting.objects.select_related('user', 'beer', 'beer__brewery', 'venue').all()
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

    def get_nearby_sightings(self, request, *args, **kwargs):
        # This implementation using foursquare is not really going to do the trick.
        # This will need implemented storing latitude and longitude for each location
        # which has a sighting locally and then figuring out the closest locally.
        latitude = request.QUERY_PARAMS.get('latitude', None)
        longitude = request.QUERY_PARAMS.get('longitude', None)

        #origin = fromstr("Point({0} {1})".format(longitude, latitude))
        origin = Point(float(longitude), float(latitude))
        queryset = self.get_queryset(prefetch=False).distance(origin, field_name='venue__point').order_by('distance')

        queryset = queryset.prefetch_related('sighting_images', 'serving_types')
        paginator = InfinitePaginator(queryset, 25)
        page_number = request.QUERY_PARAMS.get('page')
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(1)

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
        confirmation_serializer = SightingConfirmationSerializer(data={'sighting': sighting.pk, 'user': request.user.pk, 'is_available': True}, context={'request': request})
        if confirmation_serializer.is_valid():
            confirmation = confirmation_serializer.save()
            return Response(self.get_serializer(sighting).data, status=201)
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
        serializer_context = {'request': request}
        confirmation_serializer = SightingConfirmationSerializer(data={'sighting': sighting.pk, 'user': request.user.pk, 'is_available': False}, context=serializer_context)
        if confirmation_serializer.is_valid():
            confirmation = confirmation_serializer.save()
            return Response(self.get_serializer(sighting).data, status=201)
        else:
            # should return a more generic error here
            return Response(confirmation_serializer.errors, status=400)

    @action(methods=['post'])
    def add_comment(self, request, *args, **kwargs):
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

    @link()
    @cache_response(10, key_func=DefaultPaginatedListKeyConstructor())
    def comments(self, request, *args, **kwargs):
        """
        Get the comments for a sighting
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
