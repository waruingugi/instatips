# from django.test import TestCase
from datetime import datetime
from core import settings as core_settings
import requests
from core.models import Match

"""
This is a test that make a live requests to the API.
Be careful and watch for API quota usage!
Uncomment line below to run test.
"""


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

    def test_today_match_update_method(self):
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

        for fixture in fixtures:
            if fixture['fixture_id'] in matches_list:
                match = Match.objects.get(fixture_id=fixture['fixture_id'])
                match.league_id = fixture['league_id']
                match.event_date = fixture['event_date']
                match.event_timestamp = fixture['event_timestamp']
                match.firstHalfStart = fixture['firstHalfStart']
                match.secondHalfStart = fixture['secondHalfStart']
                match.roundSeason = fixture['round']
                match.status = fixture['status']
                match.statusShort = fixture['statusShort']
                match.elapsed = fixture['elapsed']
                match.venue = fixture['venue']
                match.referee = fixture['referee']
                match.homeTeam = fixture['homeTeam']
                match.awayTeam = fixture['awayTeam']
                match.goalsHomeTeam = fixture['goalsHomeTeam']
                match.goalsAwayTeam = fixture['goalsAwayTeam']
                match.score = fixture['score']

                match.save()
                # match.refresh_from_db
            else:
                new_matches_list.append(fixture)

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
                for fixture in new_matches_list
            ]

            Match.objects.bulk_create(match_instance_list)

        # Should test match model is updated
