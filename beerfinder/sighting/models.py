from django.db import models
from django.conf import settings
from django.utils import timezone

from django.contrib.gis.db import models as gis_models

from .imagekit_generators import *
from imagekit.cachefiles import ImageCacheFile, LazyImageCacheFile

class Sighting(gis_models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_sighted = models.DateTimeField(blank=True, default=timezone.now)
    venue = models.ForeignKey('venue.Venue')
    beer = models.ForeignKey('beer.Beer')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True)
    comment = models.TextField(blank=True)
    serving_types = models.ManyToManyField('beer.ServingType', blank=True, help_text="How was the beer available")

    objects = gis_models.GeoManager()

    class Meta:
        ordering = ('-date_sighted', 'beer', 'venue__name',)

    def __unicode__(self):
        return u'{0} sighted at {1} on {2}'.format(self.beer, self.venue, self.date_sighted)

    @property
    def sighted_by(self):
        if self.user.show_name_on_sightings:
            return self.user.username

        return u'Anonymous'


class SightingConfirmation(models.Model):

    sighting = models.ForeignKey(Sighting)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True)
    is_available = models.BooleanField(blank=True, default=False, db_index=True)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-date_created', 'sighting')

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    sighting = models.ForeignKey(Sighting, related_name='comments')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    text = models.TextField()

    class Meta:
        ordering = ('-date_created', 'sighting')

    def __unicode__(self):
        return u'User id {0} comment on sighting id {1}'.format(self.user_id, self.sighting_id)

    @property
    def comment_by(self):
        if self.user.show_name_on_sightings:
            return self.user.username

        return u'Anonymous'


class SightingImage(models.Model):
    """
    An image to go with a sighting with several pre-sized versions to chose from and a master
    to use for any other sizing needs.

    :ivar user: the user who uploaded the image
    :ivar sighting: the :class:`sighting.models.Sighting` the image goes with
    :date_created: when the image was uploaded
    :original: the full size, unaltered master image
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True)
    sighting = models.ForeignKey('Sighting', related_name='sighting_images')
    date_created = models.DateTimeField(auto_now_add=True, blank=True)

    original = models.ImageField(max_length=250, upload_to='sighting_images/%Y/%m/%d',
                                 height_field='original_height', width_field='original_width')
    original_height = models.IntegerField(blank=True, null=True)
    original_width = models.IntegerField(blank=True, null=True)

    thumbnail = models.ImageField(max_length=250, upload_to='sighting/images/%Y/%m/%d',
                                  blank=True, default='')
    thumbnail_height = models.IntegerField(blank=True, null=True)
    thumbnail_width = models.IntegerField(blank=True, null=True)

    small = models.ImageField(max_length=250, upload_to='sighting/images/%Y/%m/%d',
                              blank=True, default='')
    small_height = models.IntegerField(blank=True, null=True)
    small_width = models.IntegerField(blank=True, null=True)

    medium = models.ImageField(max_length=250, upload_to='sighting/images/%Y/%m/%d',
                               blank=True, default='')
    medium_height = models.IntegerField(blank=True, null=True)
    medium_width = models.IntegerField(blank=True, null=True)

    def generate_images(self):
        """
        Generate resized images from the master
        """
        if self.original:
            base_name = self.original.name

            if not self.thumbnail:
                try:
                    image_generator = SightingImageThumbnail(source=self.original)
                    filename = base_name + '.thumbnail.jpg'
                    result = ImageCacheFile(image_generator, name=filename) #.generate()
                    result.generate()
                    #self.thumbnail.save(base_name + '.thumbnail.jpg', result)
                    self.thumbnail.name = filename
                    self.save()
                finally:
                    self.original.close()
                    #self.thumbnail.close()

            if not self.small:
                try:
                    image_generator = SightingImageSmall(source=self.original)
                    filename = base_name + '.small.jpg'
                    result = ImageCacheFile(image_generator, name=filename) #.generate()
                    result.generate()
                    #self.small.save(base_name + '.small.jpg', result)
                    self.small.name = filename
                    self.save()
                finally:
                    self.original.close()
                    #self.small.close()

            if not self.medium:
                try:
                    image_generator = SightingImageMedium(source=self.original)
                    filename = base_name + '.medium.jpg'
                    result = ImageCacheFile(image_generator, name=filename) #.generate()
                    result.generate()
                    #self.medium.save(base_name + '.medium.jpg', result)
                    self.medium.name = filename
                    self.save()
                finally:
                    self.original.close()
                    #self.medium.close()

    def save(self, generate_images=False, *args, **kwargs):
        """
        Saves and then checks for the resized versions and runs
        imagekit's generate on them if they do not exist.  This is done
        rather than using ProcessedImageField for the sake of cleaner
        migrations which do not rely on imagekit being installed by referencing ProcessedImageField.

        :param generate_images: Automatically generate the resized images on save if True.  This can be problematic
          with the async backend and atomic transactions
        :type generate_images: bool
        """
        try:
            super(SightingImage, self).save(*args, **kwargs)
        except Exception, e:
            print e
            raise
        if generate_images:
            self.generate_images()
