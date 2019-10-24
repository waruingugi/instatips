from django.test import TestCase
from core.models import Leagues
from .test_data import existing_leagues_data


# Create tests here
class GetLeaguesTest(TestCase):
    def test_first_run(self):
        """
        Test first run/ creating of new leagues retrieved from response
        and saving in model.
        Note: This test only contains the create new leagues method, this
        is because once league has been set, it does not change!!!
        """
        # Those from response
        leagues = existing_leagues_data

        # Those already existing in League model
        existing_leagues = Leagues.objects.values_list('league_id', flat=True)

        new_leagues_list = []

        for league in leagues:
            if league['league_id'] not in existing_leagues:
                new_leagues_list.append(league)

        if new_leagues_list:
            leagues_instance_list = [
                Leagues(
                    league_id=league['league_id'],
                    name=league['name'],
                    country=league['country'],
                    country_code=league['country_code'],
                    season=league['season'],
                    season_start=league['season_start'],
                    season_end=league['season_end'],
                    logo=league['logo'],
                    flag=league['flag'],
                    standings=league['standings'],
                    is_current=league['is_current']
                )
                for league in new_leagues_list
            ]
            Leagues.objects.bulk_create(leagues_instance_list)

        self.assertEquals(
            Leagues.objects.all().count(),
            4
        )
