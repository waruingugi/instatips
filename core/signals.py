from core.models import (
    Countries, CountryTeam, Leagues, Match
)
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

# Initiate logging
import logging
from core import core_logger  # noqa
# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)


@receiver([post_save, post_delete], sender=Countries)
def countries_model_cache(sender, instance, **kwargs):
    all_countries_query = cache.get('all_countries_query')
    if all_countries_query:
        cache.delete('all_countries_query')
    all_countries_query = Countries.objects.all()
    cache.set('all_countries_query', all_countries_query)
    logger.info("Updated Countries Model Cache")


@receiver([post_save, post_delete], sender=Match)
def match_model_cache(sender, instance, **kwargs):
    all_matches_query = cache.get('all_matches_query')
    if all_matches_query:
        cache.delete('all_matches_query')
    all_matches_query = Match.objects.all()
    cache.set('all_matches_query', all_matches_query)
    logger.info("Updated Match Model Cache")


@receiver([post_save, post_delete], sender=Match)
def random_matches_cache(sender, instance, **kwargs):
    random_matches = cache.get('random_matches')
    if random_matches:
        cache.delete('random_matches')
    logger.info("Updated Random Matches Model Cache")


@receiver([post_save, post_delete], sender=Leagues)
def leagues_model_cache(sender, instance, **kwargs):
    all_leagues_query = cache.get('all_leagues_query')
    if all_leagues_query:
        cache.delete('all_leagues_query')
    all_leagues_query = Leagues.objects.all()
    cache.set('all_leagues_query', all_leagues_query)
    logger.info("Updated Leagues Model Cache")


@receiver([post_save, post_delete], sender=CountryTeam)
def country_team_model_cache(sender, instance, **kwargs):
    all_country_teams_query = cache.get('all_country_teams_query')
    if all_country_teams_query:
        cache.delete('all_country_teams_query')
    all_country_teams_query = CountryTeam.objects.all()
    cache.set('all_country_teams_query', all_country_teams_query)
    logger.info("Updated Country Team Model Cache")
