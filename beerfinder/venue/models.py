from django.db import models

class Venue(models.Model):

    foursquare_id = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'{0}'.format(self.foursquare_id)
