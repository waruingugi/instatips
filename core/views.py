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
    template_name = 'index.html'
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

        today_matches = all_matches.filter(event_date__range=(today, tomorrow_start))
        return today_matches
