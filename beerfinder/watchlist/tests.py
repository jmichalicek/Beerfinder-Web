from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

import factory

from accounts.tests import UserFactory
from beer.tests import BeerFactory

from .models import WatchedBeer

class WatchedBeerFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = WatchedBeer

    beer = factory.SubFactory(BeerFactory)
    user = factory.SubFactory(UserFactory)

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
