from django.forms import widgets
from rest_framework import serializers

from .models import Venue

class VenueSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Venue
        fields = ('url', 'id', 'name', 'street_address', 'city', 'state', 'postal_code', 'foursquare_id')
