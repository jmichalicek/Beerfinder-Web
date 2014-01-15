from django.db.models import Q
from rest_framework import viewsets
from rest_framework import permissions

from .models import Beer, Brewery
from .serializers import BeerSerializer, BrewerySerializer

class BeerViewSet(viewsets.ModelViewSet):
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

