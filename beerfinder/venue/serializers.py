from django.forms import widgets
from rest_framework import serializers

from .models import Venue

class VenueSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Venue
        fields = ('url', 'id', 'name', 'street_address', 'city', 'state', 'postal_code', 'latitude',
                  'longitude', 'foursquare_id')


class FoursquareVenueLocationSerializer(serializers.Serializer):
    address = serializers.CharField(source='address')
    name = serializers.CharField(source='name')
    city = serializers.CharField(source='city')
    state = serializers.CharField(source='state')
    country = serializers.CharField(source='country')
    postal_code = serializers.CharField(source='postalCode')
    is_fuzzed = serializers.CharField(source='isFuzzed')

    class Meta:
        fields = ('address', 'city', 'state', 'country', 'postal_code', 'is_fuzzed')


class FoursquareVenueSerializer(serializers.Serializer):
    id = serializers.CharField(source='id')
    location = FoursquareVenueLocationSerializer(source='location')

    class Meta:
        fields = ('id', 'name', 'location', )
