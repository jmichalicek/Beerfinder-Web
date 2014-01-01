from django.forms import widgets
from rest_framework import serializers

#from account.serializers import UserSerializer

from .models import Beer, Brewery

class BrewerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Brewery
        fields = ('id', 'name', 'slug',)


class BeerSerializer(serializers.ModelSerializer):
    brewery = BrewerySerializer()

    class Meta:
        model = Beer
        fields = ('id', 'name', 'brewery', 'slug',)
