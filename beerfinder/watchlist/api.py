from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action, link

from beer.models import Beer
#from venue.models import Venue

from .models import WatchedBeer
from .serializers import WatchedBeerSerializer, PaginatedWatchedBeerSerializer

class WatchListViewSet(viewsets.ModelViewSet):
    queryset = WatchedBeer.objects.select_related('user', 'beer', 'beer__brewery').all()
    serializer_class = WatchedBeerSerializer
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

        form_data = {'beer': beer.id, 'user': request.user.id}

        return Response()

    def pre_save(self, obj):
        obj.user = self.request.user

    def get_queryset(self):
        queryset = self.queryset
        queryset = queryset.filter(user_id=self.request.user.id)
        return queryset
