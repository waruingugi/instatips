from __future__ import absolute_import, unicode_literals
from celery import shared_task
from core.models import Countries, Leagues, Match
from core import settings as core_settings
from core.func_response_data import response_data
from datetime import datetime, timedelta

# Initiate logging
import logging
from core import core_logger  # noqa
# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)


@shared_task(name="get_countries_from_api")
def countries():
    data = None
    try:
        data = response_data(url_path=core_settings.COUNTRIES_URL).json()
    except Exception:
        """Should implement django logging here."""
        logger.critical("An error occurred in get_countries_from_api task")
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
        logger.critical("An error occurred in get_leagues_from_api task")
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
        logger.critical("An error occurred in get_today_matches_from_api task")
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


@shared_task(name='get_live_matches_from_api')
def live_matches():
    data = None
    try:
        data = response_data(url_path=core_settings.LIVE_FIXTURES_URL).json()
    except Exception:
        """Should implement django logging here."""
        logger.critical("An error occurred in get_live_matches_from_api task")
    else:
        fixtures = data['api']['fixtures']
        matches_list = Match.objects.values_list('fixture_id', flat=True)

        new_matches_list = []
        new_pending_list = []

        """
        THIS FUNCTIONALITY WILL BE UPGRADED TO FULL CAPACITY IN FUTURE.
        ---------------------------------------------------------------
        CASE 1: match in matches_list and INCLUDED_LEAGUES
                Fetch events from api and update.
        CASE 2: match in matches_list and not in INCLUDED_LEAGUES
                Update match only.
        CASE 3: match not in matches_list and in INCLUDED_LEAGUES
                Fetch events from api and create.
        CASE 4: match not in matches_list and not in INCLUDED_LEAGUES
                Create match only.
        """
        for fixture in fixtures:
            # CASE 1:
            if (
                    (fixture['fixture_id'] in matches_list) and
                    (fixture['league_id'] in core_settings.INCLUDED_LEAGUES)
            ):
                try:
                    data = response_data(url_path=core_settings.FIXTURE_URL + fixture['fixture_id']).json()
                except Exception:
                    """Should implement django logging here."""
                    logger.critical("An error occurred in CASE 1 get_live_matches_from_api task")
                else:
                    live_fixture = data['api']['fixtures'][0]

                    match = Match.objects.get(fixture_id=live_fixture['fixture_id'])
                    match.league_id = live_fixture['league_id']
                    match.event_date = live_fixture['event_date']
                    match.event_timestamp = live_fixture['event_timestamp']
                    match.firstHalfStart = live_fixture['firstHalfStart']
                    match.secondHalfStart = live_fixture['secondHalfStart']
                    match.roundSeason = live_fixture['round']
                    match.status = live_fixture['status']
                    match.statusShort = live_fixture['statusShort']
                    match.elapsed = live_fixture['elapsed']
                    match.venue = live_fixture['venue']
                    match.referee = live_fixture['referee']
                    match.homeTeam = live_fixture['homeTeam']
                    match.awayTeam = live_fixture['awayTeam']
                    match.goalsHomeTeam = live_fixture['goalsHomeTeam']
                    match.goalsAwayTeam = live_fixture['goalsAwayTeam']
                    match.score = live_fixture['score']
                    match.events = live_fixture['events'],
                    match.lineups = live_fixture['lineups'],
                    match.statistics = live_fixture['statistics'],
                    match.players = live_fixture['players']

                    match.save()

            # CASE 2:
            elif (
                (fixture['fixture_id'] in matches_list) and
                (fixture['league_id'] not in core_settings.INCLUDED_LEAGUES)
            ):
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

            # CASE 3:
            elif (
                (fixture['fixture_id'] not in matches_list) and
                (fixture['league_id'] in core_settings.INCLUDED_LEAGUES)
            ):
                new_matches_list.append(fixture)

            # CASE 4:
            else:
                new_pending_list.append(fixture)

    # CASE 3:
    if new_matches_list:
        detailed_new_matches_list = []
        for fixture in new_matches_list:
            try:
                data = response_data(url_path=core_settings.FIXTURE_URL + fixture['fixture_id']).json()
            except Exception:
                """Should implement django logging here."""
                logger.critical("An error occurred in CASE 3 get_live_matches_from_api task")
            else:
                live_fixture = data['api']['fixtures'][0]
                detailed_new_matches_list.append(live_fixture)

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
                score=fixture['score'],
                events=fixture['events'],
                lineups=fixture['lineups'],
                statistics=fixture['statistics'],
                players=fixture['players']
            )
            for fixture in detailed_new_matches_list
        ]
        Match.objects.bulk_create(match_instance_list)

    # CASE 4:
    if new_pending_list:
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
            for fixture in new_pending_list
        ]
        Match.objects.bulk_create(match_instance_list)


@shared_task(name="get_tomorrow_matches_from_api")
def tomorrow_matches():
    data = None
    try:
        tomorrow_timestamp = datetime.now() + timedelta(1)
        tomorrow = tomorrow_timestamp.strftime('%Y-%m-%d')
        data = response_data(url_path=core_settings.FIXTURE_DATE_URL + tomorrow).json()
    except Exception:
        """Should implement django logging here."""
        logger.critical("An error occurred in get_tomorrow_matches_from_api task")
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


@shared_task(name="get_day_after_tomorrow_matches_from_api")
def day_after_tomorrow_matches():
    data = None
    try:
        tomorrow_timestamp = datetime.now() + timedelta(2)
        tomorrow = tomorrow_timestamp.strftime('%Y-%m-%d')
        data = response_data(url_path=core_settings.FIXTURE_DATE_URL + tomorrow).json()
    except Exception:
        """Should implement django logging here."""
        logger.critical("An error occurred in get_day_after_tomorrow_matches_from_api task")
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
