from django.test import TestCase
# we need the user_model for the tests
from django.contrib.auth import get_user_model
# this is so we can generate the api url
from django.urls import reverse

# rest framework test helper functions

# test client we can use to make request to our API
# and see what the response is
from rest_framework.test import APIClient
# module that makes the API response
# in human readable form
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """Helper function to create users"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """
    Test the users API
    Public tests are tests that don't need authentication
    """

    def setUp(self):
        """Set up can be reused for all the tests"""
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """
        This tests the user is created successfully
        Test creating user with valid payload successful
        """
        payload = {
            'email': 'test@sidhartharoy.com',
            'password': 'testpass',
            'name': 'John Doe'
        }

        # this does an http POST request to the CREATE_USER_URL
        # to test that the outcome is what we expect
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # **res.data unpacks the response to see if
        # the user is correctly created
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        # just to make sure that the password is not returned in the response
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {
            'email': 'test@sidhartharoy.com',
            'password': 'testpass',
            'name': 'John Doe'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
        Test that the password must be more than 5 characters
        Please note that the users created in the previous test functions
        are cleared from the database. So, we can technically create the
        same user credentials again and again.
        """
        payload = {
            'email': 'shortpw@sidhartharoy.com',
            'password': 'pw',
            'name': 'John Doe'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'test@sidhartharoy.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@sidhartharoy.com', password="testpass")
        payload = {'email': 'test@sidhartharoy.com', 'password': "wrong"}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {'email': 'test@sidhartharoy.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
