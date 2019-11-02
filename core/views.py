from django.shortcuts import render
from django.views import generic
from core.models import Match
from django.core.cache import cache
from datetime import datetime, timedelta
import pytz
from core import settings as core_settings


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
            dt_now.hour-2, dt_now.minute
        )

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
