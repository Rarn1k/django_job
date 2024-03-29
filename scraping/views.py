from django.core.paginator import Paginator
from django.shortcuts import render

from .forms import FindForm
from .models import Vacancy


def home_view(request):
    form = FindForm()
    return render(request, 'scraping/home.html', {'form': form})


def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    speciality = request.GET.get('speciality')
    context = {'city': city, 'speciality': speciality, 'form': form}
    if city or speciality:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if speciality:
            _filter['speciality__slug'] = speciality

        qs = Vacancy.objects.filter(**_filter)
        paginator = Paginator(qs, 15)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(request, 'scraping/list.html', context)
