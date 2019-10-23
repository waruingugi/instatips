from django.test import TestCase
from core import settings as core_settings


# Remember to test api responses..
class CoreSettingsTest(TestCase):
    def test_api_url(self):
        api_url = 'https://api-football-v1.p.rapidapi.com/v2/'
        self.assertEqual(core_settings.API_URL, api_url)

    def test_api_headers(self):
        headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': "d901edfb17msh4441a5911a1f674p1994adjsn8397300b588f"
        }
        self.assertEqual(core_settings.HEADERS, headers)

    def test_query(self):
        query = {'timezone': 'Africa/Nairobi'}
        self.assertEqual(core_settings.QUERY_STRING, query)

    def test_get_method(self):
        get_method = 'GET'
        self.assertEqual(core_settings.HTTP_GET_METHOD, get_method)

    def test_fixture_date_url(self):
        fixture_date = 'https://api-football-v1.p.rapidapi.com/v2/fixtures/date/'
        url = core_settings.API_URL + core_settings.FIXTURE_DATE_URL
        self.assertEqual(url, fixture_date)
