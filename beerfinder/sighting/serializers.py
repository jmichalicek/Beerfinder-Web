from django.forms import widgets
from rest_framework import serializers

from .models import Sighting

class SightingSerializer(serializers.ModelSerializer):
    sighted_by = serializers.Field()
    beer = serializers.HyperlinkedRelatedField(read_only=True, view_name='beer-detail')

    class Meta:
        model = Sighting
        fields = ('id', 'date_sighted', 'venue', 'beer', 'image', 'sighted_by', )
