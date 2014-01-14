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
