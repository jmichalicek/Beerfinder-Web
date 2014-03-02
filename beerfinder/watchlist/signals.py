from django.db.models.signals import post_save
import logging

from sighting.models import Sighting

from .models import WatchedBeer
from .tasks import send_watchlist_email

logger = logging.getLogger(__name__)

def notify_watchers(sender, instance, created=False, raw=False, *args, **kwargs):
    if created and not raw:
        try:
            send_watchlist_email.delay(instance.id)
        except Exception as e:
            logger.exception(e)

post_save.connect(notify_watchers, sender=Sighting, dispatch_uid='sighting_send_email_notifications')
