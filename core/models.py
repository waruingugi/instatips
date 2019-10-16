from django.db import models
from django.contrib.postgres.fields import JSONField

# Start server using commands:
# sudo service postgresql start
# sudo -u postgres psql


# Create your models here.
class Match(models.Model):
    fixture_id = models.IntegerField()
    league_id = models.IntegerField()
    event_date = models.DateTimeField(null=True)
    event_timestamp = models.DateTimeField(null=True)
    firstHalfStart = models.DateTimeField()
    secondHalfStart = models.DateTimeField()
    roundSeason = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    statusShort = models.CharField(max_length=50)
    elapsed = models.IntegerField()
    venue = models.CharField(max_length=50)
    referee = models.CharField(max_length=50)
    homeTeam = JSONField()
    awayTeam = JSONField()
    goalsHomeTeam = models.IntegerField()
    goalsAwayTeam = models.IntegerField()
    score = JSONField()
    events = JSONField()
    lineups = JSONField()
    statistics = JSONField()
    players = JSONField()

    class Meta:
        ordering = ['-event_date']
        verbose_name_plural = ['Matches']

    def __str__(self):
        return "%s vs %s" % (self.homeTeam['name'], self.awayTeam['name'])


class Countries(models.Model):
    country = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    flag = models.URLField()

    class Meta:
        ordering = ['Country']

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
    venue_name = models.CharField(max_length=50)
    venue_surface = models.CharField(max_length=50)
    venue_address = models.CharField(max_length=50)
    venue_city = models.CharField(max_length=50)
    venue_capacity = models.IntegerField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
