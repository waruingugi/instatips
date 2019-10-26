from django.test import TestCase # noqa
from core.models import Countries, Leagues, Match
from core.tasks import countries, leagues, live_matches, today_matches


# Create tests here
# class TaskTest(TestCase):
class TaskTest():
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
        self.assertNotEqual(
            Match.objects.all().count(),
            0
        )

    def test_live_matches_task(self):
        live_matches()
        self.assertNotEqual(
            Match.objects.all().count(),
            0
        )
