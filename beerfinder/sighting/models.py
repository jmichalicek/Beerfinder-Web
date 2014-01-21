from django.db import models
from django.conf import settings
from django.utils import timezone

class Sighting(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_sighted = models.DateTimeField(blank=True, default=timezone.now)
    venue = models.ForeignKey('venue.Venue')
    beer = models.ForeignKey('beer.Beer')
    image = models.ImageField(upload_to='sighting_images/%Y/%m/%d', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True)
    comment = models.TextField(blank=True)

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
        return u'User id {0} comment on sighting id {1}'.format(self.user_id, self.id)

    @property
    def comment_by(self):
        if self.user.show_name_on_sightings:
            return self.user.username

        return u'Anonymous'
