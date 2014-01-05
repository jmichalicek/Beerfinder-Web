from django.conf import settings
from django.db import models

import foursquare

class Venue(models.Model):

    foursquare_id = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True, auto_now_add=True)
    name = models.CharField(max_length=100, blank=True)
    street_address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)


    def __unicode__(self):
        return u'{0}'.format(self.foursquare_id)

    @classmethod
    def retrieve_from_foursquare(cls, foursquare_id):
        """
        Returns an unsaved Venue() instance from Foursquare data
        """
        client_id = settings.FOURSQUARE_CLIENT_ID
        client_secret = settings.FOURSQUARE_CLIENT_SECRET
        client = foursquare.Foursquare(client_id=client_id, client_secret=client_secret)

        v = client.venues(foursquare_id)
        fs_venue = v['venue']

        venue = cls(foursquare_id=fs_venue['id'], name=fs_venue['name'],
                    street_address=fs_venue['location'].get('address', ''),
                    city=fs_venue['location'].get('city',''), state=fs_venue['location'].get('state', ''),
                    postal_code=fs_venue['location'].get('postalCode', ''), country=fs_venue['location'].get('country', ''),
                    latitude=fs_venue['location']['lat'], longitude=fs_venue['location']['lng'])
        return venue
