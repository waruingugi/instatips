# from django.shortcuts import render
from django.views import generic
from core.models import Match, Leagues
from django.core.cache import cache
from datetime import datetime, timedelta
import pytz
from core import settings as core_settings
from django.db.models import Q


# Initiate logging
import logging
from core import core_logger # noqa
# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)


# Create your views here.
class TodayListView(generic.ListView):
    model = Match
    context_object_name = 'matches'
    template_name = 'today.html'
    paginate_by = 39  # number divisible by 3 because of column-4* in large devices

    def get_queryset(self):
        """Override queryset to get only today's matches."""
        all_matches = cache.get('all_matches_query')

        if all_matches is None:
            all_matches = Match.objects.all()
            cache.set('all_matches_query', all_matches)

        timezone = pytz.timezone(core_settings.timezone)
        dt_now = datetime.now(timezone)

        """
        Set time to two hours ago to get matches being played currently,
        or just ended matches.
        """
        dt_two_hrs_ago = datetime(
            dt_now.year, dt_now.month, dt_now.day,
            dt_now.hour, dt_now.minute
        ) - timedelta(hours=2)

        upcoming_matches = []
        finished_matches = []

        """Set time range from 00:00hrs to 23:59hrs."""
        tomorrow_start = datetime(dt_now.year, dt_now.month, dt_now.day, tzinfo=timezone) + timedelta(1)
        today = datetime(dt_now.year, dt_now.month, dt_now.day, tzinfo=timezone)

        today_matches = all_matches.filter(event_date__range=(today, tomorrow_start))

        for match in today_matches:
            if match.event_timestamp > dt_two_hrs_ago:
                upcoming_matches.append(match)
            else:
                finished_matches.append(match)

        ordered_matches = upcoming_matches + finished_matches

        return ordered_matches


class TomorrowListView(generic.ListView):
    model = Match
    context_object_name = 'matches'
    template_name = 'tomorrow.html'
    paginate_by = 39  # number divisible by 3 because of column-4* in large devices

    def get_queryset(self):
        """Override queryset to get only today's matches."""
        all_matches = cache.get('all_matches_query')

        if all_matches is None:
            all_matches = Match.objects.all()
            cache.set('all_matches_query', all_matches)

        timezone = pytz.timezone(core_settings.timezone)
        dt_now = datetime.now(timezone)
        """Set time range from 00:00hrs to 23:59hrs."""
        tomorrow_start = datetime(dt_now.year, dt_now.month, dt_now.day, tzinfo=timezone) + timedelta(1)
        tomorrow_end = tomorrow_start + timedelta(1)

        tomorrow_matches = all_matches.filter(event_date__range=(tomorrow_start, tomorrow_end))
        return tomorrow_matches


class YesterdayListView(generic.ListView):
    model = Match
    context_object_name = 'matches'
    template_name = 'yesterday.html'
    paginate_by = 39  # number divisible by 3 because of column-4* in large devices

    def get_queryset(self):
        """Override queryset to get only today's matches."""
        all_matches = cache.get('all_matches_query')

        if all_matches is None:
            all_matches = Match.objects.all()
            cache.set('all_matches_query', all_matches)

        timezone = pytz.timezone(core_settings.timezone)
        dt_now = datetime.now(timezone)
        """Set time range from 00:00hrs to 23:59hrs."""
        yesterday_start = datetime(dt_now.year, dt_now.month, dt_now.day, tzinfo=timezone) - timedelta(1)
        today_start = datetime(dt_now.year, dt_now.month, dt_now.day, tzinfo=timezone)

        yesterday_matches = all_matches.filter(event_date__range=(yesterday_start, today_start))
        return yesterday_matches


class LiveListView(generic.ListView):
    model = Match
    context_object_name = 'matches'
    template_name = 'live.html'
    paginate_by = 39  # number divisible by 3 because of column-4* in large devices

    def get_queryset(self):
        """Override queryset to get only today's matches."""
        all_matches = cache.get('all_matches_query')

        if all_matches is None:
            all_matches = Match.objects.all()
            cache.set('all_matches_query', all_matches)

        timezone = pytz.timezone(core_settings.timezone)
        dt_now = datetime.now(timezone)

        """Set time range from 00:00hrs to 23:59hrs."""
        tomorrow_start = datetime(dt_now.year, dt_now.month, dt_now.day, tzinfo=timezone) + timedelta(1)
        today = datetime(dt_now.year, dt_now.month, dt_now.day, tzinfo=timezone)

        today_matches = all_matches.filter(Q(event_date__range=(today, tomorrow_start)) & (
                Q(statusShort='1H') | Q(statusShort='HT') | Q(statusShort='2H') |
                Q(statusShort='ET') | Q(statusShort='P') | Q(statusShort='AET')
            )
        )

        return today_matches


class LeagueListView(generic.ListView):
    model = Match
    context_object_name = 'leagues'
    template_name = 'leagues.html'
    paginate_by = 39  # number divisible by 3 because of column-4* in large devices

    def get_queryset(self):
        """Override queryset to get all leagues through cache"""
        all_leagues = cache.get('all_leagues_query')

        if all_leagues is None:
            all_leagues = Leagues.objects.all()
            cache.set('all_leagues_query', all_leagues)

        return all_leagues


class HighlightsListView(generic.ListView):
    model = Match
    context_object_name = 'matches'
    template_name = 'highlights.html'
    paginate_by = 39  # number divisible by 3 because of column-4* in large devices

    def get_queryset(self):
        """Get all leagues from cache."""
        all_leagues = cache.get('all_leagues_query')
        all_matches = cache.get('all_matches_query')

        if all_leagues is None:
            all_leagues = Leagues.objects.all()
            cache.set('all_leagues_query', all_leagues)

        if all_matches is None:
            all_matches = Match.objects.all()
            cache.set('all_matches_query', all_matches)

        timezone = pytz.timezone(core_settings.timezone)
        dt_now = datetime.now(timezone)
        yesterday_start = datetime(dt_now.year, dt_now.month, dt_now.day, tzinfo=timezone) - timedelta(1)

        dt_ten_hrs_ago = datetime(
            dt_now.year, dt_now.month, dt_now.day,
            dt_now.hour, dt_now.minute
        ) - timedelta(hours=10)

        random_matches = cache.get('random_matches')
        cache.delete('random_matches')

        if random_matches is None:
            current_leagues = all_leagues.filter(
                    Q(season_end__gte=yesterday_start)
                )
            random_leagues = ['Premier League', 'EFL Trophy', 'Championship']
            league_ids = []

            for league in current_leagues:
                if league.name in random_leagues:
                    league_ids.append(league.league_id)

            random_matches = all_matches.filter(
                    Q(event_timestamp__gte=yesterday_start) & Q(league_id__in=league_ids)
                )
            cache.set('random_matches', random_matches)
            logger.info("Set Random Matches Cache")

        upcoming_matches = []
        finished_matches = []

        for match in random_matches:
            if match.event_timestamp > dt_ten_hrs_ago:
                upcoming_matches.append(match)
            else:
                finished_matches.append(match)

        ordered_matches = upcoming_matches + finished_matches

        return ordered_matches
