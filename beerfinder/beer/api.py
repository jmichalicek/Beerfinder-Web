from django.db.models import Q
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response

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

from core.paginator import InfinitePaginator, InfinitePage
from core.cache_keys import DefaultPaginatedListKeyConstructor

from .forms import AddBeerForm
from .models import Beer, Brewery, ServingType, Style
from .serializers import (BeerSerializer, BrewerySerializer, ServingTypeSerializer, BeerStyleSerializer,
                          PaginatedBrewerySerializer, PaginatedBeerSerializer)



class BreweryListKeyConstructor(DefaultPaginatedListKeyConstructor):
    name = QueryParamsKeyBit(
        ['name'])


class BeerListKeyConstructor(DefaultPaginatedListKeyConstructor):
    name = QueryParamsKeyBit(
        ['name', 'brewery_name', 'search', 'page_size'])


class BeerViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    """
    Basic ViewSet for Beer API endpoints.
    """
    queryset = Beer.objects.all()
    serializer_class = BeerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    lookup_field = 'slug'
    paginate_by = 25
    paginate_by_param = 'page_size'
    list_cache_key_func = BeerListKeyConstructor()

    def pre_save(self, obj):
        obj.created_by = self.request.user

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

        try:
            beer = Beer.objects.get(name=beer_name, brewery_id=brewery.id)
            beer_created = False
        except Beer.DoesNotExist:
            self.object = Beer(name=beer_name, brewery=brewery, style=style)
            self.pre_save(self.object)
            self.object.save()
            self.post_save(self.object, created=True)
            beer_created = True

        # I think the form already handles this... oh well.
        if not beer_created:
            # simulate form errors format
            return Response({'non_field_errors': ['This beer already exists']}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance=self.object)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class BreweryAPIView(generics.ListAPIView):
    queryset = Brewery.objects.all()
    serializer_class = BrewerySerializer
    pagination_serializer_class = PaginatedBrewerySerializer
    paginator = InfinitePaginator
    paginate_by = 25

    def get_queryset(self):
        # implementing search here, but may move to its own endpoint
        # with django haystack implementing proper full text search

        queryset = super(BreweryAPIView, self).get_queryset()
        name = self.request.QUERY_PARAMS.get('name', None)
        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    @cache_response(60 * 15, key_func=BreweryListKeyConstructor())
    def get(self, request, *args, **kwargs):
        return super(BreweryAPIView, self).get(request, *args, **kwargs)


class ServingTypeAPIView(generics.ListAPIView):
    queryset = ServingType.objects.all()
    serializer_class = ServingTypeSerializer
    lookup_field = 'slug'
    paginate_by = 25

    @cache_response(60 * 15)
    def get(self, request, *args, **kwargs):
        return super(ServingTypeAPIView, self).get(request, *args, **kwargs)


class BeerStyleAPIView(generics.ListAPIView):
    queryset = Style.objects.all()
    serializer_class = BeerStyleSerializer
    paginate_by = 25

    @cache_response(60 * 15)
    def get(self, request, *args, **kwargs):
        return super(BeerStyleAPIView, self).get(request, *args, **kwargs)
