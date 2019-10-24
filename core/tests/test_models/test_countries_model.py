from django.test import TestCase
from core.models import Countries
from .test_data import countries_data


class CountriesModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        countries = countries_data

        countries_instance_list = [
            Countries(
                country=country['country'],
                code=country['code'],
                flag=country['flag']
            )
            for country in countries
        ]
        Countries.objects.bulk_create(countries_instance_list)

    def test_string_representation(self):
        country = Countries.objects.first()
        self.assertEqual(str(country), "Albania")

    def test_code_field_label(self):
        field_label = Countries._meta.get_field('code').verbose_name
        self.assertEquals(field_label, 'code')

    def test_flag_field_accepts_null_values(self):
        new_countries_data = [
            {
                'country': 'USA',
                'code': 'US',
                'flag': None
            }
        ]

        countries_instance_list = [
            Countries(
                country=country['country'],
                code=country['code'],
                flag=country['flag']
            )
            for country in new_countries_data
        ]

        Countries.objects.bulk_create(countries_instance_list)
        updated_country = Countries.objects.get(country='USA')

        self.assertEquals(
            updated_country.flag,
            None
        )

    def test_code_field_accepts_null_values(self):
        new_countries_data = [
            {
                'country': 'USA',
                'code': None,
                'flag': 'https://media.api-football.com/flags/us.svg'
            }
        ]

        countries_instance_list = [
            Countries(
                country=country['country'],
                code=country['code'],
                flag=country['flag']
            )
            for country in new_countries_data
        ]

        Countries.objects.bulk_create(countries_instance_list)
        updated_country = Countries.objects.get(country='USA')

        self.assertEquals(
            updated_country.code,
            None
        )

    def test_update_countries_model(self):
        # Test updates with new dirty data
        new_countries_data = [
            {
                'country': 'Albania',
                'code': 'AL_false',
                'flag': 'https://www.api-football.com/public/flags/al_false.svg'
            },
            {
                'country': 'Algeria',
                'code': 'DZ_false',
                'flag': 'https://www.api-football.com/public/flags/dz.svg'
            }
        ]

        for country in new_countries_data:
            country_instance = Countries.objects.get(country=country['country'])
            country_instance.code = country['code']
            country_instance.flag = country['flag']
            country_instance.save()

        updated_country = Countries.objects.first()
        self.assertEquals(
            updated_country.code,
            'AL_false'
        )
