import celery
from django.conf import settings
from django.core.mail import send_mail
from django.template import Context, Template
from django.template.loader import render_to_string

import logging

from sighting.models import Sighting

from .models import WatchedBeer

logger = logging.getLogger(__name__)

@celery.task
def send_watchlist_email(sighting_id):
    """
    Send emails about a sighting to people watching that beer
    """
    template_path = 'watchlist/email/beer_sighted.html'
    sighting = Sighting.objects.select_related('beer', 'beer_brewery').get(id=sighting_id)

    emails = WatchedBeer.objects.select_related('user').filter(beer_id=sighting.beer_id, user__send_watchlist_email=True).values_list('user__email')
    context = Context({'sighting': sighting})
    email_text = render_to_string(template_path, {}, context_instance=context)

    for email in emails:
        try:
            send_mail('A beer on your watchlist has been seen!', email_text,
                      settings.DEFAULT_FROM_EMAIL, [email[0]])
        except Exception as e:
            logger.exception(e)
