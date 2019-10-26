# from django.test import TestCase
from core import settings as core_settings
import requests
from core.models import Match


"""
THIS CODE HAS BEEN FOUND TO BE FAULTY, PLEASE REVIEW!!!
This is a test that make a live requests to the API.
Be careful and watch for API quota usage!
Uncomment line below to run test.
"""


# class GetLiveMatchesTest(TestCase):
class GetLiveMatchesTest():
    @classmethod
    def setUpTestData(cls):
        url = core_settings.API_URL + core_settings.LIVE_FIXTURES_URL
        response = requests.request(
            core_settings.HTTP_GET_METHOD,
            url,
            headers=core_settings.HEADERS,
            params=core_settings.QUERY_STRING
        )

        fixtures = response.json()['api']['fixtures']

        matches_list = Match.objects.values_list('fixture_id', flat=True)
        new_matches_list = []
        new_pending_list = []

        for fixture in fixtures:
            if (
                (fixture['fixture_id'] in matches_list) and
                (fixture['fixture_id'] in core_settings.INCLUDED_LEAGUES)
            ):
                match = Match.objects.get(fixture['fixture_id'])
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

            elif (
                (fixture['fixture_id'] not in matches_list) and
                (fixture['fixture_id'] in core_settings.INCLUDED_LEAGUES)
            ):
                new_matches_list.append(fixture)

            elif (
                (fixture['fixture_id'] in matches_list) and
                (fixture['fixture_id'] not in core_settings.INCLUDED_LEAGUES)
            ):
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
            else:
                new_pending_list.append(fixture)

        # 2.
        if new_matches_list:
            detailed_new_matches_list = []
            for fixture in new_matches_list:
                url = core_settings.API_URL + core_settings.FIXTURE_URL + fixture['fixture_id']
                response = requests.request(
                    core_settings.HTTP_GET_METHOD,
                    url,
                    headers=core_settings.HEADERS,
                    params=core_settings.QUERY_STRING
                )

                live_fixture = response.json()['api']['fixtures'][0]
                detailed_new_matches_list.append(live_fixture)

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
                    score=fixture['score'],
                    events=fixture['events'],
                    lineups=fixture['lineups'],
                    statistics=fixture['statistics'],
                    players=fixture['players']
                )
                for fixture in detailed_new_matches_list
            ]
            Match.objects.bulk_create(match_instance_list)

        # 4.
        if new_pending_list:
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
                for fixture in new_pending_list
            ]
            Match.objects.bulk_create(match_instance_list)

    def test_update_live_matches_method(self):
        url = core_settings.API_URL + core_settings.LIVE_FIXTURES_URL
        response = requests.request(
            core_settings.HTTP_GET_METHOD,
            url,
            headers=core_settings.HEADERS,
            params=core_settings.QUERY_STRING
        )

        fixtures = response.json()['api']['fixtures']

        matches_list = Match.objects.values_list('fixture_id', flat=True)

        for fixture in fixtures:
            if (
                    (fixture['fixture_id'] in matches_list) and
                    (fixture['fixture_id'] not in core_settings.INCLUDED_LEAGUES)
            ):
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

        match.refresh_from_db()

        # Should test if match objects were updated.
