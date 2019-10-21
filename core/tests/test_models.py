from django.test import TestCase
from core.models import Match
import json

# To list the test successes as well as failures:
# python manage.py test --verbosity 2


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
