import asyncio
import os
import sys
import django

from django.contrib.auth import get_user_model
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "job_search.settings"


django.setup()
from scraping.parsers import *
from scraping.models import Vacancy, Error, Url

User = get_user_model()

parsers = (
    (hh, 'hh'),
    (rabota, 'rabota'),
    (superjob, 'superjob')
)


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_list = set((q['city_id'], q['speciality_id']) for q in qs)
    return settings_list


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dict = {(q['city_id'], q['speciality_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        if pair in url_dict:
            tmp = {'city': pair[0], 'speciality': pair[1]}
            url_data = url_dict.get(pair)
            if url_data:
                tmp['url_data'] = url_dict.get(pair)
                urls.append(tmp)
    return urls


async def main(value):
    func, url, city, speciality = value
    job, error = await loop.run_in_executor(None, url, city, speciality)
    errors.extend(error)
    jobs.extend(job)


jobs, errors = [], []

settings = get_settings()
url_list = get_urls(settings)

loop = asyncio.get_event_loop()
data_tasks = [(func, elem['url_data'][key], elem['city'], elem['speciality'])
              for elem in url_list
              for func, key in parsers]
tasks = asyncio.wait([loop.create_task(main(x)) for x in data_tasks])

loop.run_until_complete(tasks)
loop.close()

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors).save()
