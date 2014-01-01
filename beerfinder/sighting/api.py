from rest_framework import viewsets
from rest_framework import permissions

from .models import Sighting
from .serializers import SightingSerializer

class SightingViewSet(viewsets.ModelViewSet):
    queryset = Sighting.objects.all()
    serializer_class = SightingSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def pre_save(self, obj):
        obj.user = self.request.user

    def get_queryset(self):
        queryset = self.queryset

        # I am not settled on this and may switch to url path params for by beer sightings
        # but then need to mess with more advanced routing
        beer_slug = self.request.QUERY_PARAMS.get('beer', None)
        if beer_slug:
            queryset = queryset.filter(beer__slug=beer_slug)

        return queryset
