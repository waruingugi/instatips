from django.test import TestCase
from core.models import Match
import json

from core.tests.test_data import fixture_id_443_events_data as fixture_events_data
from django.utils import timezone
import datetime

# To list the test successes as well as failures:
# >> python manage.py test --verbosity 2
# Test coverage
# >> coverage run --source='.' manage.py test core
# >> coverage report


# Create tests here
class MatchModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Match.objects.create(
            fixture_id=443,
            league_id=2,
            event_date="2019-05-12T14:00:00+00:00",
            event_timestamp=1557669600,
            firstHalfStart=1557669600,
            secondHalfStart=1557673200,
            roundSeason="Regular Season - 38",
            status="Match Finished",
            statusShort="FT",
            elapsed=90,
            venue="Tottenham Hotspur Stadium",
            referee=None,
            homeTeam=json.dumps(
                {
                    "team_id": 47,
                    "team_name": "Tottenham",
                    "logo": "https://media.api-football.com/teams/47.png"
                }
            ),
            awayTeam=json.dumps(
                {
                    "team_id": 45,
                    "team_name": "Everton",
                    "logo": "https://media.api-football.com/teams/45.png"
                }
            ),
            goalsHomeTeam=2,
            goalsAwayTeam=2,
            score=json.dumps(
                {
                    "halftime": "1-0",
                    "fulltime": "2-2",
                    "extratime": None,
                    "penalty": None,
                }
            )
        )

    def test_fixture_label(self):
        field_label = Match._meta.get_field('fixture_id').verbose_name
        self.assertEquals(field_label, 'fixture id')

    def test_roundSeason_label(self):
        field_label = Match._meta.get_field('roundSeason').verbose_name
        self.assertEquals(field_label, 'round')

    def test_homeTeam_team_id_field(self):
        match = Match.objects.get(fixture_id=443)
        homeTeam_data = json.loads(match.homeTeam)
        self.assertEquals(homeTeam_data['team_id'], 47)

    def test_homeTeam_team_name_field(self):
        match = Match.objects.get(fixture_id=443)
        homeTeam_data = json.loads(match.homeTeam)
        self.assertEquals(homeTeam_data['team_name'], "Tottenham")

    def test_homeTeam_team_logo_field(self):
        match = Match.objects.get(fixture_id=443)
        homeTeam_data = json.loads(match.homeTeam)
        self.assertEquals(homeTeam_data['logo'], "https://media.api-football.com/teams/47.png")

    def test_score_halftime_field(self):
        match = Match.objects.get(fixture_id=443)
        score_data = json.loads(match.score)
        self.assertEquals(score_data['halftime'], "1-0")

    def test_score_fulltime_field(self):
        match = Match.objects.get(fixture_id=443)
        score_data = json.loads(match.score)
        self.assertEquals(score_data['fulltime'], "2-2")

    def test_score_penalty_field(self):
        match = Match.objects.get(fixture_id=443)
        score_data = json.loads(match.score)
        self.assertEquals(score_data['penalty'], None)

    def test_events_update(self):
        match = Match.objects.get(fixture_id=443)
        Match.objects.filter(pk=match.pk).update(events=json.dumps(fixture_events_data))

        match.refresh_from_db()
        self.assertEquals(json.loads(match.events), fixture_events_data)

    def test_string_representation(self):
        match = Match.objects.get(fixture_id=443)
        self.assertEqual(str(match), "Tottenham vs Everton")

    def test_event_time_stamp_field(self):
        match = Match.objects.first()
        event_timestamp = timezone.get_current_timezone().localize(
            datetime.datetime.fromtimestamp(1557669600)
        )
        self.assertEqual(match.event_timestamp, event_timestamp)

    def test_secondHalfStart_field(self):
        match = Match.objects.first()
        secondHalfStart = timezone.get_current_timezone().localize(
            datetime.datetime.fromtimestamp(1557673200)
        )
        self.assertEqual(match.secondHalfStart, secondHalfStart)

    def test_get_max_league_id_method(self):
        result = Match.objects.get_max_league_id()
        self.assertEqual(result['league_id__max'], 2)
