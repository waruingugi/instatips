from django import template
import json

register = template.Library()


@register.filter(name='json_loader')
def json_loader(value, arg):
    json_data = json.loads(value)
    return json_data[arg]


@register.filter(name='minutes_format')
def minutes_format(value):
    if int(value) < 10:
        value = str(value) + "0"
    return value


@register.filter(name='hour_format')
def hour_format(value):
    if int(value) < 10:
        value = "0" + str(value)
    return value


@register.filter(name='elapsed_percentage')
def elapsed_percentage(value):
    value = (value * 100) / 90
    return value


@register.filter(name='goals_format')
def goals_format(value):
    if value is None:
        value = '-'
    return value
