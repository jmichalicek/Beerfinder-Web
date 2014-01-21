from django.forms import widgets
from rest_framework import serializers
from rest_framework import pagination

from beer.serializers import BeerSerializer
from venue.serializers import VenueSerializer

from .models import Sighting, SightingConfirmation, Comment

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


class SightingCommentSerializer(serializers.ModelSerializer):
    comment_by = serializers.Field()
    class Meta:
        model = Comment
        fields = ('date_created', 'text', 'comment_by')


class PaginatedSightingCommentSerializer(pagination.PaginationSerializer):
    """
    Does exactly what the name sounds like.  It's for paginating SightCommentSerializer
    """
    class Meta:
        object_serializer_class = SightingCommentSerializer
