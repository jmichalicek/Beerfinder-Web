from django.forms import widgets
from rest_framework import serializers
from rest_framework import pagination

from beer.serializers import BeerSerializer

from .models import Sighting, SightingConfirmation, Comment

class WatchedBeerSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.Field()
    beer = BeerSerializer()

    class Meta:
        model = Sighting
        fields = ('url', 'id', 'date_created', 'beer', 'user',)


class PaginatedWatchedBeerSerializer(pagination.PaginationSerializer):
    """
    Does exactly what the name sounds like.  It's for paginating WatchedBeerSerializer
    """
    class Meta:
        object_serializer_class = WatchedBeerSerializer
