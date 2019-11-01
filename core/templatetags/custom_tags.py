from django import template
import json
from datetime import datetime

register = template.Library()
normal_match_status = ['1H', 'HT', '2H', 'ET', 'P', 'FT',
                       'AET', 'PEN', 'BT']

# Excludes 1H and 2H from list
other_match_status = ['TBD', 'HT', 'ET', 'P', 'FT', 'AET',
                      'PEN', 'BT', 'SUSP', 'INT', 'PST', 'CANC',
                      'ABD', 'AWD', 'WO']


@register.filter(name='json_loader')
def json_loader(value, arg):
    json_data = json.loads(value)
    return json_data[arg]


@register.filter(name='elapsed_percentage')
def elapsed_percentage(value):
    value = (value * 100) / 90
    return value


@register.filter(name='goals_format')
def goals_format(value):
    if value is None:
        value = '-'
    return value


@register.filter(name='link_function')
def link_function(value):
    """
    True: url will be rendered in template.
    False: no url will be rendered.
    """
    if value in normal_match_status:
        value = True
    else:
        value = False
    return value


@register.simple_tag(name='status_or_hour')
def status_or_hour(status, time, elapsed):
    """
    Returns hour-start-time or elapsed of the match only if
    the match has no abnormality.
    """
    result = None
    elapsed = elapsed
    hour = time.hour
    if status in ['1H', '2H']:
        if int(elapsed) < 10:
            elapsed = "0" + str(elapsed)
        result = str(elapsed) + "'"

    elif status in other_match_status:
        result = status

    elif time < datetime.now() and status == 'NS':
        result = status

    else:
        if int(hour) < 10:
            hour = "0" + str(hour)
        result = str(hour) + ":"
    return result


@register.filter(name='minute_or_timestamp')
def minute_or_timestamp(status, time):
    """
    PSEUDOCODE PATTERN FOLLOWS THAT OF: status_or_hour
    Returns minute-start-time of the match only if
    the match has no abnormality.
    """
    result = None
    minutes = time.minute
    hour = time.hour

    """If minutes are less than 10 minutes, append '0' to it."""
    if int(time.minute) < 10: minutes = "0" + str(time.minute)  # noqa
    """If hour is less than 10 hours, append '0' to it."""
    if int(time.hour) < 10: hour = "0" + str(time.hour)  # noqa

    if status in ['1H', '2H']:
        result = str(hour) + ':' + str(minutes)

    elif status in other_match_status:
        "Excludes match.statusShort == 'NS'"
        result = str(hour) + ':' + str(minutes)

    elif time < datetime.now() and status == 'NS':
        result = str(hour) + ':' + str(minutes)

    else:
        result = minutes

    return result
