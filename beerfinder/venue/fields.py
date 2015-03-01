"""
DRF Fields
"""
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from rest_framework.relations import RelatedField
from django.utils.encoding import smart_text

class FoursquareIdRelatedField(RelatedField):
    """
    A read-write field the represents the :class:`venues.models.Venue` target of the relationship
    by a unique 'foursquare_id' attribute.
    """

    default_error_messages = {
        'does_not_exist': _('Object with foursquare_id={value} does not exist.'),
        'invalid': _('Invalid value.'),
    }


    def to_internal_value(self, data):
        try:
            return self.get_queryset().get(**{'foursquare_id': data})
        except ObjectDoesNotExist:
            # I'm not sure this is the best way to deal with this, but it allows
            # the serializer to look it up if it does not exist
            return data
            #self.fail('does_not_exist', value=smart_text(data))
        except (TypeError, ValueError):
            self.fail('invalid')

    def to_representation(self, obj):
        return getattr(obj, 'foursquare_id')
