from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .forms import AddBeerForm
from .models import Beer, Brewery
from .serializers import BeerSerializer, BrewerySerializer

class BeerViewSet(viewsets.ModelViewSet):
    """
    Basic ViewSet for Beer API endpoints.
    """
    queryset = Beer.objects.all()
    serializer_class = BeerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    lookup_field = 'slug'
    paginate_by = 20
    paginate_by_param = 'page_size'

    def pre_save(self, obj):
        obj.created_by = self.request.user

    def get_queryset(self):
        # implementing search here, but may move to its own endpoint
        # with django haystack implementing proper full text search
        queryset = self.queryset.select_related('brewery');
        search_term = self.request.QUERY_PARAMS.get('search', None)
        if search_term is not None and search_term.strip() != '':
            queryset = queryset.filter(Q(name__icontains=search_term) | Q(brewery__name__icontains=search_term))

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

        # just checking name directly here.  Duplicates that get created
        # due to spelling errors, etc. will get dealt with separately
        brewery, brewery_created = Brewery.objects.get_or_create(name=brewery_name)

        try:
            beer = Beer.objects.get(name=beer_name, brewery_id=brewery.id)
            beer_created = False
        except Beer.DoesNotExist:
            self.object = Beer(name=beer_name, brewery=brewery)
            self.pre_save(self.object)
            self.object.save()
            self.post_save(self.object, created=True)
            beer_created = True

        if not beer_created:
            # simulate form errors format
            return Response({'non_field_errors': ['This beer already exists']}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance=self.object)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)
