from __future__ import absolute_import, unicode_literals
from celery import shared_task
from core.models import Countries, Leagues
from core import settings as core_settings
from core.func_response_data import response_data


@shared_task(name="print_msg_with_name")
def print_message(name, *args, **kwargs):
    print("Celery is working!! {} have implemented it correctly.".format(name))


@shared_task(name="add_2_numbers")
def add(x, y):
    print("Add function has been called!! with params {}, {}".format(x, y))
    return x+y


@shared_task(name="get_countries_from_api")
def countries():
    data = None
    try:
        data = response_data(url_path=core_settings.COUNTRIES_URL).json()
    except Exception:
        """Should implement django logging here."""
        print("An error occurred in countries task!!")
    else:
        existing_countries_list = Countries.objects.values_list('country', flat=True)

        new_countries = data['api']['countries']
        new_countries_list = []

        for country in new_countries:
            if country['country'] not in existing_countries_list:
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


@shared_task(name="get_leagues_from_api")
def leagues():
    data = None
    try:
        data = response_data(url_path=core_settings.LEAGUES_URL).json()
    except Exception:
        """Should implement django logging here."""
        print("An error occurred in leagues task!!")
    else:
        # Those already existing in League model
        existing_leagues = Leagues.objects.values_list('league_id', flat=True)
        leagues = data['api']['leagues']
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
