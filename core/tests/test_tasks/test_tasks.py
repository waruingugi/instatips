from django.test import TestCase # noqa
from core.models import Countries, Leagues, Match
from datetime import datetime, timedelta
from core.tasks import (
    countries, leagues, live_matches,
    today_matches, tomorrow_matches
)


# Create tests here
class TaskTest(TestCase):
    def test_countries_task(self):
        countries()
        self.assertNotEqual(
            Countries.objects.all().count(),
            0
        )

    def test_leagues_task(self):
        leagues()
        self.assertNotEqual(
            Leagues.objects.all().count(),
            0
        )

    def test_today_matches_task(self):
        today_matches()
        match = Match.objects.first()
        self.assertEquals(
            match.event_timestamp.strftime('%Y-%m-%d'),
            datetime.now().strftime('%Y-%m-%d')
        )

    def test_tomorrow_matches_task(self):
        tomorrow_matches()
        match = Match.objects.first()
        tomorrow = datetime.now() + timedelta(1)
        self.assertEquals(
            match.event_timestamp.strftime('%Y-%m-%d'),
            tomorrow.strftime('%Y-%m-%d')
        )

    def test_live_matches_task(self):
        live_matches()
        self.assertNotEqual(
            Match.objects.all().count(),
            0
        )
