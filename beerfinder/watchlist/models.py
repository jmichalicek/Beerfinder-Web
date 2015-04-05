from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

from sighting.models import Sighting # used to connect a signal

class WatchedBeer(models.Model):
    user = models.ForeignKey('accounts.User')
    beer = models.ForeignKey('beer.Beer')
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (('user', 'beer'),)



def notify_watchers(sender, instance, created=False, raw=False, *args, **kwargs):
    from .tasks import send_watchlist_email
    if created and not raw:
        #try:
            # I'm doing something terrible here.
            # if this task executes before the database transaction which creates the sighting
            # has actually committed, then the task cannot see the sighting and so fails looking it up
            # and cannot continue.  The options to fix this are
            # 1 - Manual transaction management.  eww.  overriding django rest framework ViewSet methods, manually
            #     managing transactions in the overidden method. Yuck.
            # 2 - Pre-serialize all of the data the task needs here and pass the data as a dict into the task.
            #     More manual work, etc.
            # 3 - Fake it and just delay execution of the task for a few seconds, which is more than long enough
            #     for the commit to happen.  The task also retries 3 times with a 60 second delay if
            #     the delay here somehow wasn't enough.
            # also keep an eye on https://django-transaction-hooks.readthedocs.org/en/latest/
            # which is being considered for django core inclusion per https://code.djangoproject.com/ticket/21803
            # and nicely solves the problem.  Not sure how it will currently play with PostGIS and dj-database-url
        send_watchlist_email.apply_async([instance.id], countdown=5)
       # except Exception as e:
#            logger.exception(e)

post_save.connect(notify_watchers, sender=Sighting, dispatch_uid='sighting_send_email_notifications')
