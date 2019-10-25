from __future__ import absolute_import, unicode_literals
from celery import shared_task
from core.models import Countries, Leagues, Match
from core import settings as core_settings
from core.func_response_data import response_data
from datetime import datetime


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


@shared_task(name="get_today_matches_from_api")
def today_matches():
    data = None
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        data = response_data(url_path=core_settings.FIXTURE_DATE_URL + today).json()
    except Exception:
        """Should implement django logging here."""
        print("An error occurred in today matches task!!")
    else:
        matches_list = Match.objects.values_list('fixture_id', flat=True)
        fixtures = data['api']['fixtures']
        new_matches_list = []

        for fixture in fixtures:
            if fixture['fixture_id'] in matches_list:
                match = Match.objects.get(fixture_id=fixture['fixture_id'])
                match.league_id = fixture['league_id']
                match.event_date = fixture['event_date']
                match.event_timestamp = fixture['event_timestamp']
                match.firstHalfStart = fixture['firstHalfStart']
                match.secondHalfStart = fixture['secondHalfStart']
                match.roundSeason = fixture['round']
                match.status = fixture['status']
                match.statusShort = fixture['statusShort']
                match.elapsed = fixture['elapsed']
                match.venue = fixture['venue']
                match.referee = fixture['referee']
                match.homeTeam = fixture['homeTeam']
                match.awayTeam = fixture['awayTeam']
                match.goalsHomeTeam = fixture['goalsHomeTeam']
                match.goalsAwayTeam = fixture['goalsAwayTeam']
                match.score = fixture['score']

                match.save()
            else:
                new_matches_list.append(fixture)

        if new_matches_list:
            match_instance_list = [
                Match(
                    fixture_id=fixture['fixture_id'],
                    league_id=fixture['league_id'],
                    event_date=fixture['event_date'],
                    event_timestamp=fixture['event_timestamp'],
                    firstHalfStart=fixture['firstHalfStart'],
                    secondHalfStart=fixture['secondHalfStart'],
                    roundSeason=fixture['round'],
                    status=fixture['status'],
                    statusShort=fixture['statusShort'],
                    elapsed=fixture['elapsed'],
                    venue=fixture['venue'],
                    referee=fixture['referee'],
                    homeTeam=fixture['homeTeam'],
                    awayTeam=fixture['awayTeam'],
                    goalsHomeTeam=fixture['goalsHomeTeam'],
                    goalsAwayTeam=fixture['goalsAwayTeam'],
                    score=fixture['score']
                    )
                for fixture in new_matches_list
            ]

            Match.objects.bulk_create(match_instance_list)
