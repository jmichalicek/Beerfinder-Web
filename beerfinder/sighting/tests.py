from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone

from django.contrib.gis.geos import Point, fromstr, GEOSGeometry
from rest_framework import status
from rest_framework.test import APITestCase

import factory
from datetime import timedelta
import os

from .models import Sighting, SightingConfirmation, SightingImage

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
        self.beer1 = BeerFactory.create()
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


@override_settings(MEDIA_ROOT='/tmp/djangotests/')
@override_settings(CELERY_ALWAYS_EAGER=True)
class SightingImageViewSetTestCase(APITestCase):
    def setUp(self):
        self.beer = BeerFactory.create()
        self.user = get_user_model().objects.create_user('user@example.com', 'password')
        self.user2 = get_user_model().objects.create_user('user2@example.com', 'password')

        self.venue = VenueFactory()
        self.sighting1 = SightingFactory(beer=self.beer, venue=self.venue, user=self.user)
        self.sighting2 = SightingFactory(beer=self.beer,
                                         venue=VenueFactory.create(point=fromstr("POINT(77.29 37.33)")),
                                         date_sighted=timezone.now() - timedelta(minutes=2))

    def test_post(self):
        self.client.login(username=self.user.email, password='password')
        current_directory = os.path.dirname(os.path.realpath(__file__))
        original_image = os.path.join(current_directory, 'test_files/1000x1000.jpg')
        with open(original_image) as fp:
            post_data = {'sighting': self.sighting1.id,
                         'original': fp}
            response = self.client.post('/api/sighting_images/', post_data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        sighting_image = SightingImage.objects.get(id=response.data['id'])
        self.assertEqual(self.user, sighting_image.user)
        self.assertEqual(1000, sighting_image.original_height)
        self.assertEqual(1000, sighting_image.original_width)
        self.assertEqual(self.sighting1, sighting_image.sighting)

        self.assertEqual('http://testserver%s' % (sighting_image.original.url), response.data['original'])
        self.assertEqual('http://testserver%s' % (sighting_image.thumbnail.url), response.data['thumbnail'])
        self.assertEqual('http://testserver%s' % (sighting_image.small.url),response.data['small'])
        self.assertEqual('http://testserver%s' % (sighting_image.medium.url),response.data['medium'])
        self.assertEqual(self.sighting1.id, response.data['sighting'])
        self.assertEqual(sighting_image.id, response.data['id'])

    def test_post_logged_out(self):
        self.client.logout()
        current_directory = os.path.dirname(os.path.realpath(__file__))
        original_image = os.path.join(current_directory, 'test_files/1000x1000.jpg')
        with open(original_image) as fp:
            post_data = {'sighting': self.sighting1.id,
                         'original': fp}
            response = self.client.post('/api/sighting_images/', post_data)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_post_wrong_user(self):
        """
        Post an image for a sighting the user did not create
        """
        self.client.login(username=self.user.email, password='password')
        current_directory = os.path.dirname(os.path.realpath(__file__))
        original_image = os.path.join(current_directory, 'test_files/1000x1000.jpg')
        with open(original_image) as fp:
            post_data = {'sighting': self.sighting2.id,
                         'original': fp}
            response = self.client.post('/api/sighting_images/', post_data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual({"non_field_errors":["You may only upload images for your own sighting."]}, response.data)

    def test_delete(self):
        # TODO:  factory boy factory to create SightingImage?
        # have to be careful due to need to manually copy file
        # or watch out for real file delete when object is deleted if
        # the fiel from test_files is used directly.  This seems like
        # the least amount of work for now.
        self.client.login(username=self.user.email, password='password')
        current_directory = os.path.dirname(os.path.realpath(__file__))
        original_image = os.path.join(current_directory, 'test_files/1000x1000.jpg')
        with open(original_image) as fp:
            post_data = {'sighting': self.sighting1.id,
                         'original': fp}
            response = self.client.post('/api/sighting_images/', post_data)

            self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        sighting_id = response.data['id']
        response = self.client.delete(reverse('sightingimage-detail', args=[sighting_id]))
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertFalse(SightingImage.objects.filter(id=sighting_id).exists())

    def test_delete_not_owner(self):
        self.client.login(username=self.user.email, password='password')
        current_directory = os.path.dirname(os.path.realpath(__file__))
        original_image = os.path.join(current_directory, 'test_files/1000x1000.jpg')
        with open(original_image) as fp:
            post_data = {'sighting': self.sighting1.id,
                         'original': fp}
            response = self.client.post('/api/sighting_images/', post_data)

            self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        sighting_id = response.data['id']

        self.client.logout()
        self.client.login(username=self.user2.email, password='password')
        response = self.client.delete(reverse('sightingimage-detail', args=[sighting_id]))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertTrue(SightingImage.objects.filter(id=sighting_id).exists())
