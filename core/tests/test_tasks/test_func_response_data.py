# from django.test import TestCase
from core import settings as core_settings
from core.func_response_data import response_data

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
