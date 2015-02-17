from django.forms import widgets
from rest_framework import serializers
from rest_framework import pagination
from rest_framework.validators import CurrentUserDefault, UniqueTogetherValidator

from beer.serializers import BeerSerializer, ServingTypeSerializer
from core.serializers import InfinitePaginationSerializer
from venue.serializers import VenueSerializer

from .models import Sighting, SightingConfirmation, Comment, SightingImage

class SightingImageSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = SightingImage
        fields = ('id', 'original', 'thumbnail', 'small', 'medium',
                  'original_height', 'original_width', 'sighting', 'user')

    def __init__(self, *args, **kwargs):
        super(SightingImageSerializer, self).__init__(*args, **kwargs)
        self.fields['thumbnail'].read_only = True
        self.fields['small'].read_only = True
        self.fields['medium'].read_only = True
        self.fields['original_height'].read_only = True
        self.fields['original_width'].read_only = True

        # validate unique here, but not set on the model because I am
        # likely to allow multiple images in the future
        self.fields['sighting'].validators = [
            UniqueValidator(queryset=SightingImage.objects.all(),
                            message='Only one image allowed per Sighting')
        ]

    def validate(self, data):
        """
        Ensure that the uploader is the owner of the sighting
        """
        if data['sighting'] and data['user']:
            if not data['sighting'].user == user:
                raise serializers.ValidationError("You may only upload images for your own sighting.")
        return data


class SightingSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serialize Sighting objects
    """
    #sighted_by = serializers.Field()
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

    distance = serializers.FloatField(source='distance.mi')

    class Meta:
        model = Sighting
        fields = SightingSerializer.Meta.fields + ('distance', )


class SightingConfirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SightingConfirmation
        fields = ('is_available', 'date_created', 'user', 'sighting',)


class SightingCommentSerializer(serializers.ModelSerializer):
    #comment_by = serializers.Field()
    class Meta:
        model = Comment
        fields = ('date_created', 'text', 'comment_by')


class PaginatedSightingCommentSerializer(InfinitePaginationSerializer):
    """
    Does exactly what the name sounds like.  It's for paginating SightCommentSerializer
    """
    class Meta:
        object_serializer_class = SightingCommentSerializer


class PaginatedDistanceSightingSerializer(InfinitePaginationSerializer):
    class Meta:
        object_serializer_class = DistanceSightingSerializer


class PaginatedSightingSerializer(InfinitePaginationSerializer):
    """
    Paginated version of SightingSerializer set up for Infinite Pagination
    """
    class Meta:
        object_serializer_class = SightingSerializer


class PaginatedSightingImageSerializer(InfinitePaginationSerializer):
    """
    Paginated version of SightingImageSerializer set up for Infinite Pagination
    """
    class Meta:
        object_serializer_class = SightingImageSerializer
