from django.test import TestCase
from core.models import Leagues
from datetime import datetime
from core.tests.test_data import leagues_data


# Create tests here
class LeaguesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Leagues.objects.create(
            league_id=1,
            name="2018 Russia World Cup",
            country="World",
            country_code=None,
            season=2018,
            season_start="2018-06-14",
            season_end="2018-07-15",
            logo="https://www.api-football.com/public/leagues/1.png",
            flag=None,
            standings=0,
            is_current=1
        )

    def test_string_representation(self):
        league = Leagues.objects.get(league_id=1)
        self.assertEqual(str(league), "2018 Russia World Cup")

    def test_season_field(self):
        league = Leagues.objects.first()
        season = datetime.strptime(str(2018), '%Y').date()
        self.assertEqual(league.season.year, season.year)

    def test_season_start_field(self):
        league = Leagues.objects.first()
        season_start = datetime.strptime("2018-06-14", '%Y-%m-%d').date()
        self.assertEqual(
            datetime.date(league.season_start),
            season_start
            )

    def test_season_end_field(self):
        league = Leagues.objects.first()
        season_end = datetime.strptime("2018-07-15", '%Y-%m-%d').date()
        self.assertEqual(
            datetime.date(league.season_end),
            season_end
        )

    def test_standings_field(self):
        league = Leagues.objects.first()
        self.assertEqual(league.standings, False)

    def test_is_current_field(self):
        league = Leagues.objects.first()
        self.assertEqual(league.is_current, True)


class LeaguesModelBulkCreateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        leagues_instance_list = [
            Leagues(
                league_id=league_id,
                name=name,
                country=country,
                country_code=country_code,
                season=season,
                season_start=season_start,
                season_end=season_end,
                logo=logo,
                flag=flag,
                standings=standings,
                is_current=is_current
                )
            for league_id, name, country, country_code,
            season, season_start, season_end, logo, flag,
            standings, is_current in leagues_data
        ]
        Leagues.objects.bulk_create(leagues_instance_list)

    def test_get_max_league_id_method(self):
        result = Leagues.objects.get_max_league_id()
        self.assertEqual(result['league_id__max'], 2)
