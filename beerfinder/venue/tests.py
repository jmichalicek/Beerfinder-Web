from django.test import TestCase
from django.contrib.gis.geos import Point, fromstr, GEOSGeometry

import factory

from .models import Venue


class VenueFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Venue

    foursquare_id = factory.Sequence(lambda n: "Venue %03d" % n)
    point = fromstr("POINT(-77.29 37.33)")
