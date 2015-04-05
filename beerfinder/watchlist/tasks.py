import celery
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template import Context, Template
from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives
from django.core import mail

import logging

from sighting.models import Sighting

from .models import WatchedBeer

logger = logging.getLogger(__name__)

@celery.task(max_retries=3)
def send_watchlist_email(sighting_id):
    """
    Send emails about a sighting to people watching that beer
    """
    current_site = Site.objects.get_current()
    html_template_path = 'watchlist/email/beer_sighted.html'
    text_template_path = 'watchlist/email/beer_sighted.txt'

    try:
        sighting = Sighting.objects.select_related('beer', 'beer__brewery').get(id=sighting_id)
    except Sighting.DoesNotExist:
        # happens if the task runs but the db commit has not occured where the sighting was added
        # 60 seconds should be WAY more than enough.  Really we probably need a fraction of a second.
        raise send_watchlist_email.retry(countdown=60, exc=exc)

    emails = WatchedBeer.objects.select_related('user').filter(beer_id=sighting.beer_id, user__send_watchlist_email=True).exclude(user_id=sighting.user_id).values_list('user__email', flat=True)

    context = Context({'sighting': sighting,
                       'site': current_site})
    text_email = render_to_string(text_template_path, {}, context_instance=context)
    html_email = render_to_string(html_template_path, {}, context_instance=context)

    messages = []
    for email in emails:
        msg = EmailMultiAlternatives('A beer on your watchlist has been seen!', text_email, settings.DEFAULT_FROM_EMAIL, [email])
        msg.attach_alternative(html_email, "text/html")
        messages.append(msg)

    if messages:
        # use a single smtp connection to send all emails
        connection = mail.get_connection()
        connection.open()
        connection.send_messages(messages)
        connection.close()
