from django.forms import widgets
from rest_framework import serializers

#from account.serializers import UserSerializer

from .models import Beer, Brewery, ServingType

class BrewerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Brewery
        fields = ('id', 'name', 'slug',)


class BeerSerializer(serializers.HyperlinkedModelSerializer):
    brewery = BrewerySerializer()
    style = serializers.RelatedField() # make this SlugRelatedField?

    class Meta:
        model = Beer
        fields = ('url', 'id', 'name', 'brewery', 'style',  'slug',)


class ServingTypeSerializer(serializers.ModelSerializer):
    """
    Serializer a :class:`beer.models.ServingType`
    """

    class Meta:
        model = ServingType
        fields = ('id', 'name', 'description', 'slug')
