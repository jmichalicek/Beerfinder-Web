from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.tests import UserFactory
from beer.tests import BeerFactory

from .models import WatchedBeer

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
        watchedBeer = WatchedBeer.objects.get(id=response.data['id'])
        self.assertEqual(watchedBeer.user, self.user)
        self.assertEqual(watchedBeer.beer, self.beer)
