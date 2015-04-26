from django.db.models import Q
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response

from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.cache.mixins import CacheResponseMixin

#from core.paginator import InfinitePaginator, InfinitePage
from core.cache_keys import QueryParamsKeyConstructor

from .forms import AddBeerForm
from .models import Beer, Brewery, ServingType, Style
from .serializers import (BeerSerializer, BrewerySerializer, ServingTypeSerializer, BeerStyleSerializer)


class BeerViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    """
    Basic ViewSet for Beer API endpoints.
    """
    queryset = Beer.objects.all()
    serializer_class = BeerSerializer
#    pagination_serializer_class = PaginatedBeerSerializer
#    pagination_class = InfinitePaginator
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    lookup_field = 'slug'
    page_size = 25
    paginate_by_param = 'page_size'
    list_cache_key_func = QueryParamsKeyConstructor()

    def perform_create(self, serializer):
        """
        Enforce beer's are tied to the user who created them
        """
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        # implementing search here, but may move to its own endpoint
        # with django haystack implementing proper full text search
        queryset = self.queryset.select_related('brewery');
        search_term = self.request.QUERY_PARAMS.get('search', None)
        brewery_name = self.request.QUERY_PARAMS.get('brewery_name', None)
        name = self.request.QUERY_PARAMS.get('name', None)
        if search_term is not None and search_term.strip() != '':
            queryset = queryset.filter(Q(name__icontains=search_term)
                                       | Q(normalized_name__icontains=Beer.normalize_for_name(search_term))
                                       | Q(brewery__name__icontains=search_term)
                                       | Q(brewery__normalized_name__icontains=Brewery.normalize_for_name(search_term))
                                       )
        if brewery_name:
            queryset = queryset.filter(brewery__name__icontains=brewery_name)
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def create(self, request, *args, **kwargs):
        """
        Create a Beer model.  Also creates a brewery if necessary.
        """
        # TODO: Stop using form and use just the serializer!  Reduce logic in this method if possible
        #  This is more challenging than expected due to nested beer and brewery creation, but should be
        # able to be done more cleanly.  DRF 3.0 was supposed to simplify that, I think.

        # TODO: deal with all serializer errors!!!

        # Use standard django form or a serializer to create (but not save!) the base Beer model
        # this model may or may not have a brewery.  Perform nfkd normalization on the beer name.

        form = AddBeerForm(request.DATA)
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        beer_name = form.cleaned_data.get('beer')
        brewery_name = form.cleaned_data.get('brewery')
        style = form.cleaned_data.get('style')

        # just checking name directly here.  Duplicates that get created
        # due to spelling errors, etc. will get dealt with separately
        brewery, brewery_created = Brewery.objects.get_or_create(name=brewery_name)

        # should be able to clean this up by moving validation and lookup logic
        # to the serializer
        try:
            beer = Beer.objects.get(name=beer_name, brewery_id=brewery.id)
            beer_created = False
        except Beer.DoesNotExist:
            # TODO: use serializer and perform_create() here, don't bypass drf expected behavior!
            self.object = Beer(name=beer_name, brewery=brewery, style=style, created_by=request.user)
            self.object.save()
            beer_created = True

        # I think the form already handles this... oh well.
        if not beer_created:
            # missing lots of error conditions here!!!
            # simulate form errors format
            return Response({'non_field_errors': ['This beer already exists']}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance=self.object)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class BreweryAPIView(generics.ListAPIView):
    """
    APIView to list :class:`beer.model.Brewery`
    """
    queryset = Brewery.objects.all()
    serializer_class = BrewerySerializer
#    pagination_serializer_class = PaginatedBrewerySerializer
#    pagination_class = InfinitePaginator
    page_size = 25

    def get_queryset(self):
        # implementing search here, but may move to its own endpoint
        # with django haystack implementing proper full text search

        queryset = super(BreweryAPIView, self).get_queryset()
        name = self.request.QUERY_PARAMS.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    @cache_response(60 * 15, key_func=QueryParamsKeyConstructor())
    def get(self, request, *args, **kwargs):
        return super(BreweryAPIView, self).get(request, *args, **kwargs)


class ServingTypeAPIView(generics.ListAPIView):
    """
    View to list :class:`beer.models.ServingType`
    """

    queryset = ServingType.objects.all()
    serializer_class = ServingTypeSerializer
    lookup_field = 'slug'

    # fudging the pagination here as well because it's not really paginated
    page_size = 1000

    # again, not really paginated, so the caching does not take the page into account
    @cache_response(60 * 15)
    def get(self, request, *args, **kwargs):
        return super(ServingTypeAPIView, self).get(request, *args, **kwargs)


class BeerStyleAPIView(generics.ListAPIView):
    """
    View to list :class:`beer.models.Style`
    """

    queryset = Style.objects.all()
    serializer_class = BeerStyleSerializer

    # Don't truly want paginated, but non-paginated list returns straight list
    # while paginated returns {'results': [obj1, obj2,...]} so for consistency
    # this is paginated, but to a number that should not be hit for some time,
    # possibly not ever
    page_size = 1000

    @cache_response(60 * 15)
    def get(self, request, *args, **kwargs):
        return super(BeerStyleAPIView, self).get(request, *args, **kwargs)
