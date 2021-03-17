from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        # This will test if the there is an operational error
        # returned while testing for the database
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # patch overrides the db.utils.ConnectionHandler
            # command and always returns a true value
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    # this is to speed up the test and will always return true
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # this will raise operational error 5 times
            # and will return true the 6th time
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
