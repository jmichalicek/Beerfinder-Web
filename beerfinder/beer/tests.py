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

        response_objects = json.loads(response.content)
        self.assertEqual(len(response_objects), 2)
        self.assertEqual(response_objects[0]['id'], self.beer1.id)
        self.assertEqual(response_objects[0]['name'], self.beer1.name)

        self.assertEqual(response_objects[1]['id'], self.beer2.id)
        self.assertEqual(response_objects[1]['name'], self.beer2.name)

