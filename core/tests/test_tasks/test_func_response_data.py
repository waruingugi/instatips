from django.test import TestCase  # noqa
from core import settings as core_settings
from core.func_response_data import response_data
from datetime import datetime

"""
Test get_response_data..
Uncomment the line below to make it work
It makes live request to api
Watch out for api quota usage
"""


# class FuncResponseDataTest(TestCase):
class FuncResponseDataTest():
    def test_leagues_request(self):
        data = None
        try:
            data = response_data(url_path=core_settings.LEAGUES_URL).json()
        except Exception:
            """
            Should implement django logging here
            """
            pass
        self.assertNotEqual(data['api']['results'], 0)

    def test_countries_request(self):
        data = None
        try:
            data = response_data(url_path=core_settings.COUNTRIES_URL).json()
        except Exception:
            """
            Should implement django logging here
            """
            pass
        self.assertNotEqual(data['api']['results'], 0)

    def test_today_request(self):
        data = None
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            data = response_data(url_path=core_settings.FIXTURE_DATE_URL + today).json()
        except Exception:
            """
            Should implement django logging here
            """
            pass
        self.assertNotEqual(data['api']['results'], 0)
