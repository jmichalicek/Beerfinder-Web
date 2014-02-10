from django.db import models
from django.utils import timezone


class WatchedBeer(models.Model):
    user = models.ForeignKey('accounts.User')
    beer = models.ForeignKey('beer.Beer')
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (('user', 'beer'),)
