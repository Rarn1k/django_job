import os
import sys

from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "job_search.settings"

import django
django.setup()

from scraping.parsers import *
from scraping.models import Vacancy, City, Language, Error

parsers = (
    (hh, 'https://kazan.hh.ru/search/vacancy?area=88&search_field=name&search_field=company_name&search_field=description&text=python&from=suggest_post'),
    (rabota, 'https://kazan.rabota.ru/vacancy/?query=python&sort=relevance'),
    (superjob, 'https://kazan.superjob.ru/vacancy/search/?without_agencies=1&keywords=python')
)
city = City.objects.filter(slug='kazan').first()
language = Language.objects.filter(slug='python').first()
jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors).save()
# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()
