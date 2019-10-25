from __future__ import absolute_import, unicode_literals
from celery import shared_task
from core.models import Countries
from core import settings as core_settings
from core.func_response_data import response_data


@shared_task(name="print_msg_with_name")
def print_message(name, *args, **kwargs):
    print("Celery is working!! {} have implemented it correctly.".format(name))


@shared_task(name="add_2_numbers")
def add(x, y):
    print("Add function has been called!! with params {}, {}".format(x, y))
    return x+y


@shared_task(name="get_countries_from_api")
def countries():
    data = None
    try:
        data = response_data(url_path=core_settings.COUNTRIES_URL).json()
    except Exception:
        """Should implement django logging here."""
        print("An error occurred in countries task!!")
    else:
        existing_countries_list = Countries.objects.values_list('country', flat=True)

        new_countries = data['api']['countries']
        new_countries_list = []

        for country in new_countries:
            if country['country'] not in existing_countries_list:
                new_countries_list.append(country)

        if new_countries_list:
            countries_instance_list = [
                Countries(
                    country=country['country'],
                    code=country['code'],
                    flag=country['flag']
                )
                for country in new_countries_list
            ]
            Countries.objects.bulk_create(countries_instance_list)
