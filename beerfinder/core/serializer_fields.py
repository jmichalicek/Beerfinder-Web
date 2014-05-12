from rest_framework.fields import ImageField


class HyperlinkedImageField(ImageField):
    """
    An ImageField which returns the actual url to the image
    """
    def to_native(self, value):
        return value.url
