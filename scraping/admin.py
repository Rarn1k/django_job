from django.contrib import admin
from .models import City, Speciality, Vacancy, Error, Url

admin.site.register(City)
admin.site.register(Speciality)
admin.site.register(Vacancy)
admin.site.register(Error)
admin.site.register(Url)
