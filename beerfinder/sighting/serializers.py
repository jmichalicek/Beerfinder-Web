from django.forms import widgets
from rest_framework import serializers
from rest_framework import pagination
from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import UniqueValidator

from beer.models import Beer, ServingType
from beer.serializers import BeerSerializer, ServingTypeSerializer
from core.serializers import InfinitePaginationSerializer
from venue.fields import FoursquareIdRelatedField
from venue.models import Venue
from venue.serializers import VenueSerializer

from .models import Sighting, SightingConfirmation, Comment, SightingImage

class SightingImageSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = SightingImage
        fields = ('id', 'original', 'thumbnail', 'small', 'medium',
                  'original_height', 'original_width', 'sighting', 'user')
        read_only_fields = ('thumbnail', 'small', 'medium', 'original_height',
                            'original_width')

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
        Ensure that the uploader is the owner of the sighting (which should really be
        a permissions and http 403 response situation)
        """
        if data['sighting'] and data['user']:
            if not data['sighting'].user == data['user']:
                raise serializers.ValidationError("You may only upload images for your own sighting.")
        return data


class SightingSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serialize Sighting objects
    """
    #sighted_by = serializers.Field()
    beer = BeerSerializer(read_only=True)
    venue = VenueSerializer(read_only=True)
    # if serving_types and serving_type_ids both directly refer to obj.serving_types
    # then the serializer blows up thinking that we are trying to write a nested field and
    # says to set read_only=True.  That happens even if read_only=True is already set.
    # To work around that this read_only serving_types is a SerializerMethodField which
    # will spit out the correct data.
    serving_types = serializers.SerializerMethodField(read_only=True) #ServingTypeSerializer(read_only=True, many=True)
    images = SightingImageSerializer(source='sighting_images', many=True, read_only=True)

    venue_foursquare_id = FoursquareIdRelatedField(queryset=Venue.objects.all(),
                                                   write_only=True,
                                                   source='venue')
    beer_slug = serializers.SlugRelatedField(source='beer',
                                             write_only=True,
                                             queryset=Beer.objects.all(),
                                             slug_field='slug')
    serving_type_ids = serializers.PrimaryKeyRelatedField(queryset=ServingType.objects.all(),
                                                          write_only=True, many=True, source='serving_types')

    class Meta:
        model = Sighting
        fields = ('url', 'id', 'date_sighted', 'venue', 'beer', 'serving_types', 'images',
                  'sighted_by', 'comment', 'venue_foursquare_id', 'beer_slug',
                  'serving_type_ids',)

    def get_serving_types(self, obj):
        serving_types = obj.serving_types
        return ServingTypeSerializer(serving_types, many=True).data

    def validate_venue_foursquare_id(self, value):
        # Maybe the magic of the FoursquareIdRelatedField should be removed
        # and this could just be a CharField which converts?  That's also a bit
        # unclear.  It could also just save an additional object on the serializer.
        if not isinstance(value, Venue):
            # or value is true, but not the right thing?
            venue = Venue.retrieve_from_foursquare(value)
            venue.save()
            value = venue
        return value


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
