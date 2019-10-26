from django.test import TestCase
from core.models import CountryTeam
from .test_data import country_teams_data


class CountryTeamModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        country_teams_instance_list = [
            CountryTeam(
                team_id=team['team_id'],
                name=team['name'],
                code=team['code'],
                logo=team['logo'],
                country=team['country'],
                founded=team['founded'],
                venue_name=team['venue_name'],
                venue_surface=team['venue_surface'],
                venue_address=team['venue_address'],
                venue_city=team['venue_city'],
                venue_capacity=team['venue_capacity']
                )
            for team in country_teams_data
        ]
        CountryTeam.objects.bulk_create(country_teams_instance_list)

    def test_string_representation(self):
        country_team = CountryTeam.objects.first()
        self.assertEqual(str(country_team), 'Kariobangi Sharks')
