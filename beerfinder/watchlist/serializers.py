from django.forms import widgets
from rest_framework import serializers
from rest_framework import pagination

from beer.serializers import BeerSerializer

from .models import WatchedBeer


class WatchedBeerSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.Field()
    beer = BeerSerializer(read_only=True)

    class Meta:
        model = WatchedBeer
        fields = ('url', 'id', 'date_added', 'beer', 'user',)

# is there a better way to do this?
class WatchedBeerWriteableSerializer(WatchedBeerSerializer):
    """
    User for adding watched beers because we need to handle the beer field
    differently here than when reading/listing
    """

    beer = serializers.SlugRelatedField(write_only=True, slug_field='slug')

    class Meta:
        model = WatchedBeer
        fields = ('url', 'id', 'date_added', 'beer', 'user',)


class PaginatedWatchedBeerSerializer(pagination.PaginationSerializer):
    """
    Does exactly what the name sounds like.  It's for paginating WatchedBeerSerializer
    """
    class Meta:
        object_serializer_class = WatchedBeerSerializer
