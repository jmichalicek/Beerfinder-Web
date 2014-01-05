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
