from django.shortcuts import render

from .forms import FindForm
from .models import Vacancy


def home_view(request):
    form = FindForm()
    city = request.GET.get('city')
    speciality = request.GET.get('speciality')
    qs = []
    if city or speciality:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if speciality:
            _filter['speciality__slug'] = speciality

        qs = Vacancy.objects.filter(**_filter)
    return render(request, 'scraping/home.html', {'object_list': qs, 'form': form})
