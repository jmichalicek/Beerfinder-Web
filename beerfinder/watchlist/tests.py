from django.test import TestCase
from django.test.utils import override_settings
from django.core import mail
from rest_framework import status
from rest_framework.test import APITestCase

import factory

from accounts.tests import UserFactory
from beer.tests import BeerFactory
from sighting.tests import SightingFactory
from venue.tests import VenueFactory

from .models import WatchedBeer
from .tasks import send_watchlist_email


class WatchedBeerFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = WatchedBeer

    beer = factory.SubFactory(BeerFactory)
    user = factory.SubFactory(UserFactory)


@override_settings(CELERY_ALWAYS_EAGER=True)
class APIWatchListTest(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.beer = BeerFactory()

    def test_post(self):
        self.client.login(username=self.user.username, password='password')

        post_data = {
            'beer': self.beer.slug}

        response = self.client.post('/api/watchlist/', data=post_data)
        #TODO: find way to have beer returned from this request
        watched_beer = WatchedBeer.objects.get(id=response.data['id'])
        self.assertEqual(watched_beer.user, self.user)
        self.assertEqual(watched_beer.beer, self.beer)

    def test_get(self):

        # to ensure that only the correct user's watched beers shows up
        user2 = UserFactory.create()
        user2_watched = WatchedBeerFactory.create(user=user2, beer=self.beer)

        self.client.login(username=self.user.username, password='password')
        watched_beer = WatchedBeerFactory.create(user=self.user, beer=self.beer)

        response = self.client.get('/api/watchlist/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], watched_beer.id)

    def test_delete(self):
        user2 = UserFactory.create()
        user2_watched = WatchedBeerFactory.create(user=user2, beer=self.beer)

        self.client.login(username=self.user.username, password='password')
        watched_beer = WatchedBeerFactory.create(user=self.user, beer=self.beer)

        response = self.client.delete('/api/watchlist/{0}/'.format(watched_beer.id))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(WatchedBeer.objects.filter(id=watched_beer.id).exists())

        # now try to delete someone else's
        response = self.client.delete('/api/watchlist/{0}/'.format(user2_watched.id))
        self.assertEqual(response.status_code, 404)


@override_settings(CELERY_ALWAYS_EAGER=True)
class SendWatchlistEmailTest(TestCase):

    def setUp(self):
        self.venue = VenueFactory()

    def test_send_emails(self):
        """
        Tests the celery task specifically.
        Testing that emails are sent when a sighting is created with no regard
        to the method will be done separately.
        """
        user_1 = UserFactory.create()
        user_2 = UserFactory.create()
        user_3 = UserFactory.create()

        beer_1 = BeerFactory.create()
        beer_2 = BeerFactory.create()

        user_1_watched_1 = WatchedBeerFactory.create(user=user_1, beer=beer_1)
        user_2_watched_1 = WatchedBeerFactory.create(user=user_2, beer=beer_1)
        user_2_watched_1 = WatchedBeerFactory.create(user=user_2, beer=beer_2)

        beer_1_sighting = SightingFactory.create(user=user_3, beer=beer_1, venue=self.venue)
        beer_2_sighting = SightingFactory.create(user=user_3, beer=beer_2, venue=self.venue)

        mail.outbox = []
        send_watchlist_email.delay(beer_1_sighting.id)
        self.assertEqual(len(mail.outbox), 2)
        recipients = [m.to for m in mail.outbox]
        self.assertItemsEqual(recipients, [[user_1.email], [user_2.email]])

        mail.outbox = []
        send_watchlist_email.delay(beer_2_sighting.id)
        self.assertEqual(len(mail.outbox), 1)
        for m in mail.outbox:
            self.assertEqual(m.to, [user_2.email])

        user_1.send_watchlist_email = False
        user_1.save()
        mail.outbox = []
        send_watchlist_email.delay(beer_1_sighting.id)
        self.assertEqual(len(mail.outbox), 1)
        for m in mail.outbox:
            self.assertEqual(m.to, [user_2.email])


@override_settings(CELERY_ALWAYS_EAGER=True)
class WatchlistTest(TestCase):
    def setUp(self):
        self.venue = VenueFactory()
        self.user = UserFactory()
        self.user_2 = UserFactory.create()
        self.beer = BeerFactory()
        self.watched_beer = WatchedBeerFactory(user=self.user, beer=self.beer)

    def test_email_sent_on_sighting(self):
        """
        Test that emails are sent to user's watching a beer when a sighting is created
        """
        mail.outbox = []
        SightingFactory.create(user=self.user_2, beer=self.beer, venue=self.venue)
        self.assertEqual(len(mail.outbox), 1)
        for m in mail.outbox:
            self.assertEqual(m.to, [self.user.email])
