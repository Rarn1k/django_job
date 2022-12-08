import os
import sys

from django.contrib.auth import get_user_model
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "job_search.settings"

import django

django.setup()

from scraping.parsers import *
from scraping.models import Vacancy, City, Speciality, Error, Url

User = get_user_model()

parsers = (
    (hh,
     'https://kazan.hh.ru/search/vacancy?area=88&search_field=name&search_field=company_name&search_field=description&text=python&from=suggest_post'),
    (rabota, 'https://kazan.rabota.ru/vacancy/?query=python&sort=relevance'),
    (superjob, 'https://kazan.superjob.ru/vacancy/search/?without_agencies=1&keywords=python')
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
            tmp = {'city': pair[0], 'language': pair[1]}
            url_data = url_dict.get(pair)
            if url_data:
                tmp['url_data'] = url_dict.get(pair)
                urls.append(tmp)
    return urls


q = get_settings()
u = get_urls(q)
city = City.objects.filter(slug='kazan').first()
speciality = Speciality.objects.filter(slug='python').first()
jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(**job, city=city, speciality=speciality)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors).save()
# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()
