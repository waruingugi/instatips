from django.db import models
from django.contrib.postgres.fields import JSONField
from core.managers import CustomManager

import datetime
import re
import json
from django.utils import timezone
from dateutil.parser import parse

# Start server using commands:
# >> sudo service postgresql start
# >> sudo -u postgres psql
# Other commands are:
# >> ALTER USER instatips_admin CREATEDB;


# Create your models here.
class Match(models.Model):
    objects = CustomManager()

    fixture_id = models.IntegerField(unique=True)
    league_id = models.IntegerField()
    event_date = models.DateTimeField(null=True)
    event_timestamp = models.DateTimeField(null=True)
    firstHalfStart = models.DateTimeField(null=True)
    secondHalfStart = models.DateTimeField(null=True)
    roundSeason = models.CharField("round", max_length=100)
    status = models.CharField(max_length=100)
    statusShort = models.CharField(max_length=10)
    elapsed = models.IntegerField()
    venue = models.CharField(null=True, max_length=100)  # noqa
    referee = models.CharField(max_length=100, null=True)  # noqa
    homeTeam = JSONField(null=True)
    awayTeam = JSONField(null=True)
    goalsHomeTeam = models.IntegerField(null=True)
    goalsAwayTeam = models.IntegerField(null=True)
    score = JSONField(null=True)
    events = JSONField(null=True)
    lineups = JSONField(null=True)
    statistics = JSONField(null=True)
    players = JSONField(null=True)

    class Meta:
        ordering = ['event_date']
        verbose_name_plural = ['Matches']

    def __str__(self):
        return "%s vs %s" % (
            json.loads(self.homeTeam)['team_name'],
            json.loads(self.awayTeam)['team_name']
        )

    def save(self, *args, **kwargs):
        """
        Calls field_conversions before save.
        """
        self.field_conversions()
        super().save(*args, **kwargs)

    def field_conversions(self):
        """
        Performs conversions that allow data to be saved in fields.
        """
        # if statements ensure no conversions are done on null values
        if self.event_date:
            self.event_date = timezone.get_current_timezone().localize(
                datetime.datetime(
                *map(int, re.split('[^\d]', self.event_date)[:-1]))  # noqa
            )
        if self.event_timestamp:
            self.event_timestamp = timezone.get_current_timezone().localize(
                datetime.datetime.fromtimestamp(self.event_timestamp)
            )
        if self.firstHalfStart:
            self.firstHalfStart = timezone.get_current_timezone().localize(
                datetime.datetime.fromtimestamp(self.firstHalfStart)
            )
        if self.secondHalfStart:
            self.secondHalfStart = timezone.get_current_timezone().localize(
                datetime.datetime.fromtimestamp(self.secondHalfStart)
            )
        self.homeTeam = json.dumps(self.homeTeam)
        self.awayTeam = json.dumps(self.awayTeam)
        self.score = json.dumps(self.score)


# List all countries
class Countries(models.Model):
    country = models.CharField(max_length=100)
    code = models.CharField(max_length=10, null=True)  # noqa
    flag = models.URLField(null=True)  # noqa

    class Meta:
        ordering = ['country']

    def __str__(self):
        return self.country


# List all teams in country.
class CountryTeam(models.Model):
    team_id = models.IntegerField()
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    logo = models.URLField()
    country = models.CharField(max_length=100)
    founded = models.IntegerField()
    venue_name = models.CharField(max_length=100, null=True)  # noqa
    venue_surface = models.CharField(max_length=100, null=True)  # noqa
    venue_address = models.CharField(max_length=100, null=True)  # noqa
    venue_city = models.CharField(max_length=100, null=True)  # noqa
    venue_capacity = models.IntegerField(null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# List all leagues
class Leagues(models.Model):
    objects = CustomManager()

    league_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10, null=True)  # noqa
    season = models.DateTimeField()  # YYYY
    season_start = models.DateTimeField()  # YYYY-MM-DD
    season_end = models.DateTimeField()  # YYYY-MM-DD
    logo = models.URLField(null=True)  # noqa
    flag = models.URLField(null=True)  # noqa
    standings = models.BooleanField()
    is_current = models.BooleanField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Calls field_conversions before save.
        """
        self.field_conversions()
        super().save(*args, **kwargs)

    def field_conversions(self):
        """
        Performs date_time conversions that allow string data to be saved in fields.
        """
        self.season = timezone.get_current_timezone().localize(
            parse(str(self.season))
        )
        self.season_start = timezone.get_current_timezone().localize(
            parse(self.season_start)
        )
        self.season_end = timezone.get_current_timezone().localize(
            parse(self.season_end)
        )
        self.standings = bool(self.standings)
        self.is_current = bool(self.is_current)
