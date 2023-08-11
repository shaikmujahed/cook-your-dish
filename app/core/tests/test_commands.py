"""
Test custom django management commands
"""
from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# Command.check method provided by base command class to check the db
# checking the command inside the patch
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """"Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """"Test waiting for database if database ready."""
        """patched_check parameter is magic mock object
            replace check by patch"""
        patched_check.return_value = True
        call_command('wait_for_db')
        # execute the code inside wait_for_db module
        patched_check.assert_called_once_with(databases=['default'])
        # ensure that check call with databse=['default']

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError"""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
