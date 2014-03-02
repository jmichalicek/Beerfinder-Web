from django.test import TestCase

import factory

from .models import Venue


class VenueFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Venue

    foursquare_id = factory.Sequence(lambda n: "Venue %03d" % n)
