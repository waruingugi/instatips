from django.test import TestCase
from core.models import Countries
from .test_data import existing_countries_data, new_countries_data


# Create tests here
class GetCountriesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        existing_countries = existing_countries_data

        countries_instance_list = [
            Countries(
                country=country['country'],
                code=country['code'],
                flag=country['flag']
            )
            for country in existing_countries
        ]
        Countries.objects.bulk_create(countries_instance_list)

    def test_only_existing_countries_in_model(self):
        self.assertEquals(
            Countries.objects.all().count(),
            17
        )

    def test_new_countries_code(self):
        new_countries = new_countries_data
        countries_list = Countries.objects.values_list('country', flat=True)
        new_countries_list = []

        for country in new_countries:
            if country['country'] not in countries_list:
                new_countries_list.append(country)

        if new_countries_list:
            countries_instance_list = [
                Countries(
                    country=country['country'],
                    code=country['code'],
                    flag=country['flag']
                )
                for country in new_countries_list
            ]
            Countries.objects.bulk_create(countries_instance_list)

        self.assertEquals(
            Countries.objects.all().count(),
            33
        )
