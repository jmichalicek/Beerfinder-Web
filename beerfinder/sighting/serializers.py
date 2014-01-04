from django.forms import widgets
from rest_framework import serializers

from beer.serializers import BeerSerializer

from .models import Sighting

class SightingSerializer(serializers.HyperlinkedModelSerializer):
    sighted_by = serializers.Field()
    beer = BeerSerializer()
    venue = serializers.RelatedField() # TODO: write a VenueSerializer

    class Meta:
        model = Sighting
        fields = ('url', 'id', 'date_sighted', 'venue', 'beer', 'image', 'sighted_by', 'comment',)
