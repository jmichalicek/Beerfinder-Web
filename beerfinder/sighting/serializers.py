from django.forms import widgets
from rest_framework import serializers

from beer.serializers import BeerSerializer
from venue.serializers import VenueSerializer

from .models import Sighting, SightingConfirmation

class SightingSerializer(serializers.HyperlinkedModelSerializer):
    sighted_by = serializers.Field()
    beer = BeerSerializer()
    venue = VenueSerializer()

    class Meta:
        model = Sighting
        fields = ('url', 'id', 'date_sighted', 'venue', 'beer', 'image', 'sighted_by', 'comment',)


class SightingConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SightingConfirmation
        fields = ('is_available', 'date_created', 'user', 'sighting',)
