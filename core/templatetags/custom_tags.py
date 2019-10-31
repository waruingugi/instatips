from django import template
import json

register = template.Library()
normal_match_status = ['1H', 'HT', '2H', 'ET', 'P', 'FT',
                       'AET', 'PEN', 'BT']


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


@register.filter(name='status_or_hour')
def status_or_hour(status, hour):
    """
    Returns hour-start-time of the match only if
    the match has no abnormality.
    """
    result = None
    if status not in normal_match_status:
        result = status
    else:
        if int(hour) < 10:
            hour = "0" + str(hour) + ":"
        result = hour
    return result


@register.filter(name='minute_or_timestamp')
def minute_or_timestamp(status, time):
    """
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

    if status not in normal_match_status:
        result = str(hour) + ':' + str(minutes)
    else:
        result = minutes
    return result
