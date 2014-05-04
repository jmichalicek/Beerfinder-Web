from django.test import TestCase
from django.contrib.auth import get_user_model

import factory
from factory.django import DjangoModelFactory
import simplejson as json

from accounts.tests import UserFactory

from .models import Beer, Brewery


class BreweryFactory(DjangoModelFactory):
    FACTORY_FOR = Brewery

    name = factory.Sequence(lambda n: "Brewery %03d" % n)

class BeerFactory(DjangoModelFactory):
    FACTORY_FOR = Beer

    name = factory.Sequence(lambda n: "Beer %03d" % n)
    brewery = factory.SubFactory(BreweryFactory)
    created_by = factory.SubFactory(UserFactory)


class BeerTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.beer = BeerFactory()

    def test_unicode(self):
        self.assertEqual(self.beer.__unicode__(), self.beer.name)

    def test_attributes(self):
        """
        Test for expected attributes on the model
        """
        expected_attributes = ['name', 'brewery']
        for attribute in expected_attributes:
            self.assertTrue(hasattr(self.beer, attribute), "Beer model is missing expected attribute {0}".format(attribute))

    def test_normalize_for_name(self):
        """
        Test the Beer.normalize_for_name static method
        """
        original = u"""This  has. extra\tpunctuation and
whitespace characters_wheee---!"""
        normalized = Beer.normalize_for_name(original)
        self.assertEqual("This has extra punctuation and whitespace characterswheee", normalized)

    def test_save(self):
        """
        Tests that a slug is created and a normalized_name is created
        and that whitespace and punctuation have been properly stripped out.
        """
        brewery = BreweryFactory(name='A  Brewery')
        beer = Beer(name='A  beer!',
                    brewery=brewery,
                    created_by=self.user)
        beer.save()
        self.assertEqual(beer.slug, 'a-brewery-a-beer')
        self.assertEqual(beer.normalized_name, 'A beer')


class BreweryTestCase(TestCase):
    def setUp(self):
        self.brewery = BreweryFactory()

    def test_unicode(self):
        self.assertEqual(self.brewery.__unicode__(), self.brewery.name)

    def test_attributes(self):
        """
        Test for expected attributes on the model
        """

        expected_attributes = ['name', ]
        for attribute in expected_attributes:
            self.assertTrue(hasattr(self.brewery, attribute), "Brewery model is missing expected attribute {0}".format(attribute))

    def test_normalize_for_name(self):
        """
        Test the Beer.normalize_for_name static method
        """
        original = u"""This  has. extra\tpunctuation and
whitespace characters_wheee---!"""
        normalized = Beer.normalize_for_name(original)
        self.assertEqual("This has extra punctuation and whitespace characterswheee", normalized)

    def test_save(self):
        """
        Tests that a slug is created and a normalized_name is created
        and that whitespace and punctuation have been properly stripped out.
        """
        brewery = Brewery(name='A  brewery!')
        brewery.save()
        self.assertEqual(brewery.slug, 'a-brewery')
        self.assertEqual(brewery.normalized_name, 'A brewery')


class BeerViewSetTestCase(TestCase):
    """
    Test the BeerViewSet and routes to it
    """

    def setUp(self):
        self.beer1 = BeerFactory()
        self.beer2 = BeerFactory()
        self.user = get_user_model().objects.create_user('user@example.com', 'password')

    def test_get_list(self):
        self.client.login(username=self.user.email, password='password')
        response = self.client.get('/api/beer/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        response_objects = json.loads(response.content)['results']
        self.assertEqual(len(response_objects), 2)
        self.assertEqual(response_objects[0]['id'], self.beer1.id)
        self.assertEqual(response_objects[0]['name'], self.beer1.name)

        self.assertEqual(response_objects[1]['id'], self.beer2.id)
        self.assertEqual(response_objects[1]['name'], self.beer2.name)

    def test_create(self):
        """
        Test /api/beer/ POST to create a new beer with just name and brewery name
        """
        self.client.login(username=self.user.email, password='password')

        post_data = {'beer': 'Duff Beer!',
                     'brewery': 'Duff\t'
                     }
        response = self.client.post('/api/beer/', data=post_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response['Content-Type'], 'application/json')

        response_object = json.loads(response.content)
        self.assertTrue(response_object['id'])
        self.assertEqual(response_object['name'], 'Duff Beer!')
        self.assertEqual(response_object['slug'], 'duff-duff-beer')
        self.assertEqual(response_object['url'], 'http://testserver/api/beer/duff-duff-beer/')
        self.assertEqual(response_object['brewery']['name'], 'Duff')
        self.assertEqual(response_object['brewery']['slug'], 'duff')

    def test_create_not_logged_in(self):
        """
        Try to create a beer with POST to /api/beer/ when not logged in
        """
        self.client.logout()
        post_data = {'beer': 'Duff Beer!',
                     'brewery': 'Duff\t'
                     }
        response = self.client.post('/api/beer/', data=post_data)
        # returns a 403 rather than 401 when not logged in due to tastypie internals
        # probably because anonymouse user is "authenticated" as being the anonymous user?
        self.assertEqual(response.status_code, 403)
