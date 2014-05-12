from django.forms import widgets
from rest_framework import serializers
from rest_framework import pagination

from beer.serializers import BeerSerializer, ServingTypeSerializer
from core.serializer_fields import HyperlinkedImageField
from venue.serializers import VenueSerializer

from .models import Sighting, SightingConfirmation, Comment, SightingImage

class SightingImageSerializer(serializers.ModelSerializer):
    original = HyperlinkedImageField(allow_empty_file=True)
    thumbnail = HyperlinkedImageField(allow_empty_file=True)
    small = HyperlinkedImageField(allow_empty_file=True)
    medium = HyperlinkedImageField(allow_empty_file=True)

    class Meta:
        model = SightingImage
        fields = ('id', 'original', 'thumbnail', 'small', 'medium', 'original_height', 'original_width')


class SightingSerializer(serializers.HyperlinkedModelSerializer):
    sighted_by = serializers.Field()
    beer = BeerSerializer()
    venue = VenueSerializer()
    serving_types = ServingTypeSerializer(many=True)
    images = SightingImageSerializer(source='sighting_images', many=True)

    class Meta:
        model = Sighting
        fields = ('url', 'id', 'date_sighted', 'venue', 'beer', 'images', 'sighted_by', 'comment', 'serving_types')


class DistanceSightingSerializer(SightingSerializer):
    """
    Sighting with distance from user

    Possibly this should just always be used and Sighting should always return distance.
    """

    distance = serializers.Field()

    class Meta:
        model = Sighting
        fields = SightingSerializer.Meta.fields + ('distance', )

    def transform_distance(self, obj, value):
        return obj.distance.mi


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


class PaginatedDistanceSightingSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = DistanceSightingSerializer
