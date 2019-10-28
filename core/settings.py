# SETTINGS FOR TASKS AND OTHER MODULES IN CORE APP.

API_URL = 'https://api-football-v1.p.rapidapi.com/v2/'
HEADERS = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "d901edfb17msh4441a5911a1f674p1994adjsn8397300b588f"
    }

FIXTURE_DATE_URL = 'fixtures/date/'
LIVE_FIXTURES_URL = 'fixtures/live'
FIXTURE_URL = 'fixtures/id/'
LEAGUES_URL = 'leagues'
COUNTRIES_URL = 'countries'

QUERY_STRING = {'timezone': 'Africa/Nairobi'}
timezone = 'Africa/Nairobi'

EUROPE_TZ = 'Europe/London'
AFRICA_TZ = 'Africa/Nairobi'

INCLUDED_LEAGUES = []

HTTP_GET_METHOD = 'GET'

SERVER_SIDE_ERROR_CODES = [
    501, 502, 503, 504, 505, 506,
    507, 508, 510, 511, 500, 521, 522,
]
