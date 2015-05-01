from django.forms import widgets
from rest_framework import serializers
from rest_framework import pagination

from accounts.models import User
from beer.models import Beer
from beer.serializers import BeerSerializer

from .models import WatchedBeer


class WatchedBeerSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    beer = BeerSerializer(read_only=True)
    # TODO: I think I need to make user a PrimaryKeyRelaedField or stop using HyperlinkedModelSerializer

    class Meta:
        model = WatchedBeer
        fields = ('url', 'id', 'date_added', 'beer', 'user',)

# is there a better way to do this?
class WatchedBeerWriteableSerializer(WatchedBeerSerializer):
    """
    User for adding watched beers because we need to handle the beer field
    differently here than when reading/listing
    """

    beer = serializers.SlugRelatedField(write_only=True, slug_field='slug', queryset=Beer.objects.all())

    class Meta:
        model = WatchedBeer
        fields = ('url', 'id', 'date_added', 'beer')


#class PaginatedWatchedBeerSerializer(pagination.PaginationSerializer):
#    """
#    Does exactly what the name sounds like.  It's for paginating WatchedBeerSerializer
#    """
#    class Meta:
#        object_serializer_class = WatchedBeerSerializer
