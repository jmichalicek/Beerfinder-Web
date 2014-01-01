from rest_framework import viewsets
from rest_framework import permissions

from .models import Beer, Brewery
from .serializers import BeerSerializer, BrewerySerializer

class BeerViewSet(viewsets.ModelViewSet):
    queryset = Beer.objects.all()
    serializer_class = BeerSerializer
    permission_classes = (permissions.IsAuthenticated, )
    lookup_field = 'slug'

    def pre_save(self, obj):
        obj.created_by = self.request.user
