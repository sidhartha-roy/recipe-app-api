from django.test import TestCase
from django.contrib.auth import get_user_model
# this generated urls for the django admin userlist
from django.urls import reverse
# create a test client that will make
# request to the url for unit tests
from django.test import Client


# create a test class
class AdminSiteTests(TestCase):

    def setUp(self):
        """Setup tasks needed to run the tests"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@sidhartharoy.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@sidhartharoy.com',
            password='password123',
            name='testfirstname testlastname'
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""

        # an url is create using a reverse helper function
        # these urls are listed in the django admin documentation
        # these generates an url for our list user page
        url = reverse('admin:core_user_changelist')
        # this uses the test client to perform a
        # http get request on the url
        res = self.client.get(url)

        # this checks that the response contains a certain item
        # it checks that the http response is 200 and looks for the output
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/

        res = self.client.get(url)

        # response 200 is OK that the page worked
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
