from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models import Max

import datetime
import re
from django.utils import timezone

# Start server using commands:
# >> sudo service postgresql start
# >> sudo -u postgres psql
# Other commands are:
# >> ALTER USER instatips_admin CREATEDB;


# Create your models here.
class Match(models.Model):
    fixture_id = models.IntegerField(unique=True)
    league_id = models.IntegerField()
    event_date = models.DateTimeField(null=True)
    event_timestamp = models.DateTimeField(null=True)
    firstHalfStart = models.DateTimeField(null=True)
    secondHalfStart = models.DateTimeField(null=True)
    roundSeason = models.CharField("Round", max_length=50)
    status = models.CharField(max_length=50)
    statusShort = models.CharField(max_length=50)
    elapsed = models.IntegerField()
    venue = models.CharField(max_length=50)
    referee = models.CharField(max_length=50, null=True)  # noqa
    homeTeam = JSONField()
    awayTeam = JSONField()
    goalsHomeTeam = models.IntegerField()
    goalsAwayTeam = models.IntegerField()
    score = JSONField(null=True)
    events = JSONField(null=True)
    lineups = JSONField(null=True)
    statistics = JSONField(null=True)
    players = JSONField(null=True)

    class Meta:
        ordering = ['-event_date']
        verbose_name_plural = ['Matches']

    def __str__(self):
        return "%s vs %s" % (self.homeTeam['name'], self.awayTeam['name'])

    def save(self, *args, **kwargs):
        """
        Performs conversions that allow data to be saved in fields.
        """
        self.event_date = timezone.get_current_timezone().localize(
            datetime.datetime(
            *map(int, re.split('[^\d]', self.event_date)[:-1]))  # noqa
        )
        self.event_timestamp = timezone.get_current_timezone().localize(
            datetime.datetime.fromtimestamp(self.event_timestamp)
        )
        self.firstHalfStart = timezone.get_current_timezone().localize(
            datetime.datetime.fromtimestamp(self.firstHalfStart)
        )
        self.secondHalfStart = timezone.get_current_timezone().localize(
            datetime.datetime.fromtimestamp(self.secondHalfStart)
        )
        super().save(*args, **kwargs)


class Countries(models.Model):
    country = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    flag = models.URLField()

    class Meta:
        ordering = ['country']

    def __str__(self):
        return self.country


# List all teams in country.
class CountryTeam(models.Model):
    team_id = models.IntegerField()
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    logo = models.URLField()
    country = models.CharField(max_length=50)
    founded = models.IntegerField()
    venue_name = models.CharField(max_length=50, null=True)  # noqa
    venue_surface = models.CharField(max_length=50, null=True)  # noqa
    venue_address = models.CharField(max_length=50, null=True)  # noqa
    venue_city = models.CharField(max_length=50, null=True)  # noqa
    venue_capacity = models.IntegerField(null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# List all leagues
class Leagues(models.Model):
    league_id = models.IntegerField()
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    country_code = models.CharField(max_length=10)
    season = models.IntegerField()  # YYYY
    season_start = models.CharField(max_length=50)  # YYYY-MM-DD
    season_end = models.CharField(max_length=50)  # YYYY-MM-DD
    logo = models.URLField()
    flag = models.URLField()
    standings = models.IntegerField()
    is_current = models.IntegerField()

    class Meta:
        ordering = ['league_id']

    def __str__(self):
        return self.name

    def get_max_league_id(self):
        """
        Get the latest league id e.g if league id's are 1,2,3
        then return 3 as the highest league id.
        """
        return Leagues.objects.all().aggregate(Max('league_id'))
