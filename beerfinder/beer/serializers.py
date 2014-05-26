from django.forms import widgets
from rest_framework import serializers

#from account.serializers import UserSerializer
from core.serializers import InfinitePaginationSerializer
from .models import Beer, Brewery, ServingType, Style

class BrewerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Brewery
        fields = ('id', 'name', 'slug',)


class PaginatedBrewerySerializer(InfinitePaginationSerializer):
    class Meta:
        object_serializer_class = BrewerySerializer


class BeerStyleSerializer(serializers.ModelSerializer):
    """
    Serializer for :class:`beer.models.Style`
    """

    class Meta:
        model = Style
        fields = ('id', 'name', 'slug')


class BeerSerializer(serializers.HyperlinkedModelSerializer):
    brewery = BrewerySerializer()
    style = BeerStyleSerializer() # make this SlugRelatedField?

    class Meta:
        model = Beer
        fields = ('url', 'id', 'name', 'brewery', 'style',  'slug',)


class PaginatedBeerSerializer(InfinitePaginationSerializer):
    class Meta:
        object_serializer_class = BeerSerializer


class ServingTypeSerializer(serializers.ModelSerializer):
    """
    Serializer a :class:`beer.models.ServingType`
    """

    class Meta:
        model = ServingType
        fields = ('id', 'name', 'description', 'slug')
