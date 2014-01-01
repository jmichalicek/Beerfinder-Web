from django.test import TestCase

import factory

from .models import User

class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = User

    email = factory.Sequence(lambda n: "user_%03d@example.com" % n)
    is_active = True
    is_staff = False
    is_superuser = False
    show_name_on_sightings = True
