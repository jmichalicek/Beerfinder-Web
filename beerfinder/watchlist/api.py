from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from .models import WatchedBeer
from .serializers import WatchedBeerSerializer, WatchedBeerWriteableSerializer

class WatchListViewSet(viewsets.ModelViewSet):
    queryset = WatchedBeer.objects.select_related('user', 'beer', 'beer__brewery').all()
    serializer_class = WatchedBeerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    page_size = 25
    paginate_by_param = 'page_size'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(user_id=self.request.user.id)
        return queryset

    def get_serializer_class(self):
        """
        Returns the normal serializer for read type requests.
        Return the serializer which takes beer slug for write requests.
        """
        if self.request.method not in ['POST', 'PUT']:
            return super(WatchListViewSet, self).get_serializer_class()
        else:
            return WatchedBeerWriteableSerializer
