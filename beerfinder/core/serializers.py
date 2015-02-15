from rest_framework import serializers, pagination
from rest_framework.fields import ImageField


class NextPageNumberField(serializers.Field):
    """
    Field that returns the next page number in paginated results
    """
    page_field = 'page'

    def to_native(self, value):
        return self.to_representation(value)

    def to_representation(self, value):
        if not value.has_next():
            return None
        return value.next_page_number()


class PreviousPageNumberField(serializers.Field):
    """
    Field that returns the previous page number in paginated results.
    """
    page_field = 'page'

    def to_native(self, value):
        return self.to_represenatation(value)

    def to_representation(self, value):
        if not value.has_previous():
            return None
        page = value.previous_page_number()
        return page


class InfinitePaginationSerializer(pagination.BasePaginationSerializer):
    next = NextPageNumberField(source='*')
    previous = PreviousPageNumberField(source='*')
