import datetime
import os
import sys

import django
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

from job_search.settings import EMAIL_HOST_USER

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "job_search.settings"

django.setup()

from scraping.models import Vacancy, Error, Url

ADMIN_USER = EMAIL_HOST_USER

today = datetime.date.today()
subject = f"Рассылка вакансий за {today}"
text_content = f"Рассылка вакансий"
from_email = EMAIL_HOST_USER
empty = '<h2>К сожалению, на сегодня не на нашлось профессий по Вашим предпочтениям.</h2>'

User = get_user_model()
qs = User.objects.filter(send_email=True).values('city', 'speciality', 'email')

users_dct = {}
for i in qs:
    users_dct.setdefault((i['city'], i['speciality']), [])
    users_dct[(i['city'], i['speciality'])].append(i['email'])
if users_dct:
    params = {'city_id__in': [], 'speciality_id__in': []}
    for pair in users_dct.keys():
        params['city_id__in'].append(pair[0])
        params['speciality_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params, timestamp=today).values()
    vacancies = {}
    for vac in qs:
        vacancies.setdefault((vac['city_id'], vac['speciality_id']), [])
        vacancies[(vac['city_id'], vac['speciality_id'])].append(vac)
    for keys, emails in users_dct.items():
        rows = vacancies.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h3"><a href="{row["url"]}">{row["title"]}</a></h3>'
            html += f'<p>{row["description"]} </p>'
            html += f'<p>{row["company"]} </p><br><hr>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()


qs = Error.objects.filter(timestamp=today)
subject = ''
text_content = ''
to = ADMIN_USER
_html = ''
if qs.exists():
    error = qs.first()
    data = error.data.get('errors', [])
    for i in data:
        _html += f'<p"><a href="{i["url"]}">Error: {i["title"]}</a></p><br>'
    subject += f"Ошибки скрапинга {today}"
    text_content += "Ошибки скрапинга"
    data = error.data.get('user_data')
#     if data:
#         _html += '<hr>'
#         _html += '<h2>Пожелания пользователей </h2>'
#         for i in data:
#             _html += f'<p">Город: {i["city"]}, Специальность:{i["language"]},  Имейл:{i["email"]}</p><br>'
#         subject += f" Пожелания пользователей {today}"
#         text_content += "Пожелания пользователей"
#
qs = Url.objects.all().values('city', 'speciality')
urls_dct = {(i['city'], i['speciality']): True for i in qs}
urls_err = ''
for keys in users_dct.keys():
    if keys not in urls_dct:
        if keys[0] and keys[1]:
            urls_err += f'<p"> Для города: {keys[0]} и ЯП: {keys[1]} отсутствуют ссылки</p><br>'
if urls_err:
    subject += ' Отсутствующие ссылки '
    _html += '<hr>'
    _html += '<h2>Отсутствующие ссылки </h2>'
    _html += urls_err

if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()
