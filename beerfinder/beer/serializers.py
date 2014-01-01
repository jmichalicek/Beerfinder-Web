from django.forms import widgets
from rest_framework import serializers

#from account.serializers import UserSerializer

from .models import Beer, Brewery

class BrewerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Brewery
        fields = ('id', 'name', 'slug',)


class BeerSerializer(serializers.HyperlinkedModelSerializer):
    brewery = BrewerySerializer()

    class Meta:
        model = Beer
        fields = ('url', 'id', 'name', 'brewery', 'slug',)
