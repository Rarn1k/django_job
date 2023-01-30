from django import forms

from scraping.models import City, Speciality


class FindForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name='slug', required=False,
                                  widget=forms.Select(attrs={'class': 'form-control'}), label='Город')
    speciality = forms.ModelChoiceField(queryset=Speciality.objects.all(), to_field_name='slug', required=False,
                                        widget=forms.Select(attrs={'class': 'form-control'}),
                                        label='Специальность')
