from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from django.contrib.gis.geos import Point, fromstr, GEOSGeometry
from rest_framework.test import APITestCase

import factory
from datetime import timedelta

from .models import Sighting, SightingConfirmation

from beer.tests import BeerFactory
from accounts.tests import UserFactory
from venue.tests import VenueFactory

class AnonymousUserFactory(UserFactory):
    show_name_on_sightings = False

class SightingFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Sighting

    user = factory.SubFactory(UserFactory)

class AnonymousSightingFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Sighting

    user = factory.SubFactory(AnonymousUserFactory)


class SightingTestCase(TestCase):

    def setUp(self):
        self.beer = BeerFactory()
        self.venue = VenueFactory()
        self.sighting = SightingFactory(beer=self.beer, venue=self.venue)
        self.anonymous_sighting = AnonymousSightingFactory(beer=self.beer, venue=self.venue)

        self.user = self.sighting.user

    def test_sighted_by(self):
        self.assertEqual(self.sighting.sighted_by, self.sighting.user.email)
        self.assertEqual(self.anonymous_sighting.sighted_by, 'Anonymous')

    def test_save(self):
        beer = BeerFactory()
        past_sighting_time = timezone.now() - timedelta(days=2)

        now_sighting = Sighting(beer=beer, user=self.user, venue=self.venue)
        past_sighting = Sighting(beer=beer, user=self.user, date_sighted=past_sighting_time, venue=self.venue)

        now_sighting.save()
        # There is a tiny bit of time between when now_sighting.save() gets the current datetime and when our test does
        # so it is impossible to test that they are truly equal.  Instead allow for a small marging of error, but close enough
        # that it must be the same thing.
        self.assertTrue(timezone.now() - now_sighting.date_sighted < timedelta(seconds=2))

        past_sighting.save()
        self.assertEqual(past_sighting.date_sighted, past_sighting_time)


class SightingViewSetTestCase(APITestCase):
    # legend Point("-77.4429997801781 37.5268217786912")
    # hardywood Point("-77.4419362313172 37.5254898040785")
    # the national Point("-77.4352025985718 37.5418168540823")

    def setUp(self):
        self.beer2 = BeerFactory.create()
        self.user = get_user_model().objects.create_user('user@example.com', 'password')

        self.venue = VenueFactory()
        self.beer1_sighting1 = SightingFactory(beer=self.beer1, venue=self.venue)
        self.beer2_sighting1 = SightingFactory(beer=self.beer2, venue=self.venue, date_sighted=timezone.now() - timedelta(minutes=1))
        self.beer1_sighting2 = SightingFactory(beer=self.beer1, venue=VenueFactory.create(point = fromstr("POINT(77.29 37.33)")
), date_sighted=timezone.now() - timedelta(minutes=2))
        self.beer2_sighting2 = SightingFactory(beer=self.beer2, venue=VenueFactory.create(point=fromstr("Point(-77.4419362313172 37.5254898040785)")), user=UserFactory(show_name_on_sightings=False), date_sighted=timezone.now() - timedelta(minutes=3))

    def test_get_list(self):
        """
        Get the full list of sightings
        """

        self.client.login(username=self.user.email, password='password')
        response = self.client.get('/api/sightings/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        response_objects = response.data['results']
        self.assertEqual(len(response_objects), 4)

        self.assertEqual(response_objects[0]['id'], self.beer1_sighting1.id)
        self.assertEqual(response_objects[0]['sighted_by'], self.beer1_sighting1.user.email)
        self.assertEqual(response_objects[0]['beer']['slug'], self.beer1.slug)
        self.assertEqual(response_objects[0]['beer']['url'], 'http://testserver/api/beer/{0}/'.format(self.beer1.slug))

        self.assertEqual(response_objects[1]['id'], self.beer2_sighting1.id)
        self.assertEqual(response_objects[1]['sighted_by'], self.beer2_sighting1.user.email)
        self.assertEqual(response_objects[1]['beer']['slug'], self.beer2.slug)

        self.assertEqual(response_objects[2]['id'], self.beer1_sighting2.id)
        self.assertEqual(response_objects[2]['sighted_by'], self.beer1_sighting2.user.email)
        self.assertEqual(response_objects[2]['beer']['slug'], self.beer1.slug)

        self.assertEqual(response_objects[3]['id'], self.beer2_sighting2.id)
        self.assertEqual(response_objects[3]['sighted_by'], 'Anonymous')
        self.assertEqual(response_objects[3]['beer']['slug'], self.beer2.slug)

    def test_get_list_by_beer(self):
        """
        Get the sightings for a specific beer filtered by slug
        """

        self.client.login(username=self.user.email, password='password')
        response = self.client.get('/api/sightings/?beer={0}'.format(self.beer1.slug))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        response_objects = response.data['results']
        self.assertEqual(len(response_objects), 2)

        self.assertEqual(response_objects[0]['id'], self.beer1_sighting1.id)
        self.assertEqual(response_objects[0]['sighted_by'], self.beer1_sighting1.user.email)
        self.assertEqual(response_objects[0]['beer']['slug'], self.beer1.slug)
        self.assertEqual(response_objects[0]['beer']['url'], 'http://testserver/api/beer/{0}/'.format(self.beer1.slug))

        self.assertEqual(response_objects[1]['id'], self.beer1_sighting2.id)
        self.assertEqual(response_objects[1]['sighted_by'], self.beer1_sighting2.user.email)
        self.assertEqual(response_objects[1]['beer']['slug'], self.beer1.slug)

    def test_confirm_available(self):
        self.client.login(username=self.user.email, password='password')
        current_confirmation_count = self.beer1_sighting1.sightingconfirmation_set.filter(is_available=True).count()
        response = self.client.post('/api/sightings/{0}/confirm_available/'.format( self.beer1_sighting1.id))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Content-Type'], 'application/json')
        updated_confirmation_count = self.beer1_sighting1.sightingconfirmation_set.filter(is_available=True).count()
        self.assertTrue(updated_confirmation_count == current_confirmation_count + 1)

    def test_confirm_unavailable(self):
        self.client.login(username=self.user.email, password='password')
        unavailable_confirmation_count = self.beer1_sighting1.sightingconfirmation_set.filter(is_available=False).count()
        response = self.client.post('/api/sightings/{0}/confirm_unavailable/'.format( self.beer1_sighting1.id))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Content-Type'], 'application/json')
        updated_unavailable_count = self.beer1_sighting1.sightingconfirmation_set.filter(is_available=False).count()
        self.assertTrue(updated_unavailable_count == unavailable_confirmation_count + 1)


class SightingImageViewSetTestCase(APITestCase):
    def setUp(self):
        self.beer2 = BeerFactory.create()
        self.user = get_user_model().objects.create_user('user@example.com', 'password')

        self.venue = VenueFactory()
        self.beer1_sighting1 = SightingFactory(beer=self.beer1, venue=self.venue)
        self.beer2_sighting1 = SightingFactory(beer=self.beer2, venue=self.venue,
                                               date_sighted=timezone.now() - timedelta(minutes=1))
        self.beer1_sighting2 = SightingFactory(beer=self.beer1,
                                               venue=VenueFactory.create(point=fromstr("POINT(77.29 37.33)")),
                                               date_sighted=timezone.now() - timedelta(minutes=2))
        self.beer2_sighting2 = SightingFactory(beer=self.beer2,
                                               venue=VenueFactory.create(
                                                   point=fromstr("Point(-77.4419362313172 37.5254898040785)")),
                                               user=UserFactory(show_name_on_sightings=False),
                                               date_sighted=timezone.now() - timedelta(minutes=3))

    def test_post(self):
        self.client.login(username=self.user.email, password='password')
