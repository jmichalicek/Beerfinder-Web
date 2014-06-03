from django.test import TestCase
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.test import APITestCase

import factory

from .models import User
from .serializers import AllDataUserSerializer

DEFAULT_PASSWORD = 'password'

class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = User

    email = factory.Sequence(lambda n: "user_%03d@example.com" % n)
    is_active = True
    is_staff = False
    is_superuser = False
    show_name_on_sightings = True
    first_name = factory.Sequence(lambda n: "first_%03d" % n)
    last_name = factory.Sequence(lambda n: "last_%03d" % n)

    @factory.post_generation
    def set_password(obj, create, extracted, **kwargs):
        obj.set_password(DEFAULT_PASSWORD)
        obj.save()


class MyProfileViewTest(TestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_get(self):
        self.client.login(username=self.user.username, password=DEFAULT_PASSWORD)
        response = self.client.get('/accounts/my_profile/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.user)

    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get('/accounts/my_profile')
        # this must be something django-allauth is doing.  Pretty sure django
        # does a 302 normally and I think a 302 is more correct
        self.assertEqual(response.status_code, 301)


class AllDataUserSerializerTest(TestCase):

    def test_fields(self):
        fields = ('id', 'email', 'username', 'date_joined', 'first_name', 'last_name', 'show_name_on_sightings', 'send_watchlist_email')

        self.assertEqual(fields, AllDataUserSerializer.Meta.fields)

    def test_model(self):
        self.assertEqual(User, AllDataUserSerializer.Meta.model)

    def test_serializer(self):
        user = UserFactory()
        serialized = AllDataUserSerializer(user)
        self.assertEqual(serialized.data['id'], user.id)
        self.assertEqual(serialized.data['email'], user.email)
        self.assertEqual(serialized.data['username'], user.username)
        self.assertEqual(serialized.data['date_joined'], user.date_joined)
        self.assertEqual(serialized.data['first_name'], user.first_name)
        self.assertEqual(serialized.data['last_name'], user.last_name)
        self.assertEqual(serialized.data['show_name_on_sightings'], user.show_name_on_sightings)
        self.assertEqual(serialized.data['send_watchlist_email'], user.send_watchlist_email)


class UserProfileAPIViewTest(APITestCase):

    def setUp(self):
        self.user = UserFactory.create()
        self.user_2 = UserFactory.create(show_name_on_sightings=False)

    def test_get(self):
        self.client.login(username=self.user.email, password=DEFAULT_PASSWORD)
        response = self.client.get('/api/account/profile/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['date_joined'], self.user.date_joined)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)
        self.assertEqual(response.data['show_name_on_sightings'], self.user.show_name_on_sightings)
        self.assertEqual(response.data['send_watchlist_email'], self.user.send_watchlist_email)

        self.client.logout()
        self.client.login(username=self.user_2.email, password=DEFAULT_PASSWORD)
        response = self.client.get('/api/account/profile/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user_2.id)
        self.assertEqual(response.data['email'], self.user_2.email)
        self.assertEqual(response.data['username'], self.user_2.username)
        self.assertEqual(response.data['date_joined'], self.user_2.date_joined)
        self.assertEqual(response.data['first_name'], self.user_2.first_name)
        self.assertEqual(response.data['last_name'], self.user_2.last_name)
        self.assertEqual(response.data['show_name_on_sightings'], self.user_2.show_name_on_sightings)
        self.assertEqual(response.data['send_watchlist_email'], self.user_2.send_watchlist_email)

    def test_change_email(self):
        self.client.login(username=self.user.email, password=DEFAULT_PASSWORD)
        response = self.client.post('/api/account/profile/me/', data={'email': 'fake@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'fake@example.com')
        self.assertEqual(response.data['id'], self.user.id)

        updated = User.objects.get(pk=self.user.pk)
        self.assertEqual(updated.email, 'fake@example.com')

    def test_change_email_already_taken(self):
        self.client.login(username=self.user.email, password=DEFAULT_PASSWORD)
        response = self.client.post('/api/account/profile/me/', data={'email': self.user_2.email})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"email": ["User with this Email address already exists."]})

        # Make sure it really didn't change
        updated = User.objects.get(pk=self.user.pk)
        self.assertEqual(updated.email, self.user.email)

    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get('/api/account/profile/me/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post('/api/account/profile/me/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class ChangePasswordApiViewAPIViewTest(APITestCase):

    def setUp(self):
        self.user = UserFactory.create()
        self.user_2 = UserFactory.create(show_name_on_sightings=False)

    def test_not_logged_in(self):
        self.client.logout()
        response = self.client.get('/api/account/profile/change_password/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post('/api/account/profile/change_password/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get(self):
        self.client.login(username=self.user.email, password=DEFAULT_PASSWORD)
        response = self.client.get('/api/account/profile/change_password/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post(self):
        self.client.login(username=self.user.email, password=DEFAULT_PASSWORD)
        form_data = {
            'oldpassword': DEFAULT_PASSWORD,
            'password1': 'asdf123',
            'password2': 'asdf123'}

        response = self.client.post('/api/account/profile/change_password/', data=form_data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        user = authenticate(username=self.user.username, password='asdf123')
        self.assertIsNotNone(user)
        self.assertEqual(user, self.user)

    def test_post_bad_data(self):
        self.client.login(username=self.user.email, password=DEFAULT_PASSWORD)
        form_data = {
            'oldpassword': 'BAD PASSWORD',
            'password1': 'asdf123',
            'password2': 'asdf123'}

        response = self.client.post('/api/account/profile/change_password/', data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"oldpassword": ["Please type your current password."]})

        # missing fields
        form_data = {
            }
        response = self.client.post('/api/account/profile/change_password/', data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"password1": ["This field is required."], "password2": ["This field is required."], "oldpassword": ["This field is required."]})

        form_data = {
            'oldpassword': DEFAULT_PASSWORD,
            'password1': 'asdf1234',
            'password2': 'asdf123'}

        response = self.client.post('/api/account/profile/change_password/', data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"password2": ["You must type the same password each time."]})
