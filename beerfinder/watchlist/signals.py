from django.db.models.signals import post_save

from sighting.models import Sighting

from .models import WatchedBeer
from .tasks import send_watchlist_twitter_dm

def notify_watchers(sender, instance, created=False, raw=False, *args, **kwargs):
    if not created and not raw:
        send_watchlist_twitter_dm.delay(instance.beer_id)

post_save.connect(asdf, sender=Sighting, uid='sighting_send_notifications')
