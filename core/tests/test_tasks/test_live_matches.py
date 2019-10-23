# from django.test import TestCase
from datetime import datetime
from core import settings as core_settings
import requests
from core.models import Match


# Uncomment line below to test functionality
# class GetTodayMatchesTest(TestCase):
class GetTodayMatchesTest():
    @classmethod
    def setUpTestData(cls):
        today = datetime.now().strftime('%Y-%m-%d')

        url = core_settings.API_URL + core_settings.FIXTURE_DATE_URL + today
        response = requests.request(
            core_settings.HTTP_GET_METHOD,
            url,
            headers=core_settings.HEADERS,
            params=core_settings.QUERY_STRING
        )

        fixtures = response.json()['api']['fixtures']

        matches_list = Match.objects.values_list('fixture_id', flat=True)
        new_matches_list = []
        existing_matches_list = []

        for fixture in fixtures:
            if fixture['fixture_id'] in matches_list:
                existing_matches_list.append(fixture)
            else:
                new_matches_list.append(fixture)

        if existing_matches_list:
            match_instance_list = [
                Match(
                    fixture_id=fixture['fixture_id'],
                    league_id=fixture['league_id'],
                    event_date=fixture['event_date'],
                    event_timestamp=fixture['event_timestamp'],
                    firstHalfStart=fixture['firstHalfStart'],
                    secondHalfStart=fixture['secondHalfStart'],
                    round=fixture['round'],
                    status=fixture['status'],
                    statusShort=fixture['statusShort'],
                    elapsed=fixture['elapsed'],
                    venue=fixture['venue'],
                    referee=fixture['referee'],
                    homeTeam=fixture['homeTeam'],
                    awayTeam=fixture['awayTeam'],
                    goalsHomeTeam=fixture['goalsHomeTeam'],
                    goalsAwayTeam=fixture['goalsAwayTeam'],
                    score=fixture['score']
                    )
                for fixture in fixtures
            ]
            Match.objects.bulk_update(match_instance_list)

        if new_matches_list:
            match_instance_list = [
                Match(
                    fixture_id=fixture['fixture_id'],
                    league_id=fixture['league_id'],
                    event_date=fixture['event_date'],
                    event_timestamp=fixture['event_timestamp'],
                    firstHalfStart=fixture['firstHalfStart'],
                    secondHalfStart=fixture['secondHalfStart'],
                    roundSeason=fixture['round'],
                    status=fixture['status'],
                    statusShort=fixture['statusShort'],
                    elapsed=fixture['elapsed'],
                    venue=fixture['venue'],
                    referee=fixture['referee'],
                    homeTeam=fixture['homeTeam'],
                    awayTeam=fixture['awayTeam'],
                    goalsHomeTeam=fixture['goalsHomeTeam'],
                    goalsAwayTeam=fixture['goalsAwayTeam'],
                    score=fixture['score']
                    )
                for fixture in fixtures
            ]

            Match.objects.bulk_create(match_instance_list)

    def test_get_max_league_id_method(self):
        result = Match.objects.get_max_league_id()
        self.assertEqual(result['league_id__max'], 2)
