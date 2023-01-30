from django.db import models

from scraping.utility import from_cyrillic_to_eng


def default_urls():
    return {"hh": '', "rabota": '', "superjob": ''}


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название населенного пункта', unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Название населенного пункта'
        verbose_name_plural = 'Название населенных пунктов'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Speciality(models.Model):
    name = models.CharField(max_length=50, verbose_name='Специальность', unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Специальности'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Название вакансии')
    company = models.CharField(max_length=250, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    speciality = models.ForeignKey('Speciality', on_delete=models.CASCADE, verbose_name='Специальность')
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-timestamp']


    def __str__(self):
        return self.title


class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = models.JSONField()

    def __str__(self):
        return str(self.timestamp)


class Url(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='Город')
    speciality = models.ForeignKey('Speciality', on_delete=models.CASCADE, verbose_name='Специальность')
    url_data = models.JSONField(default=default_urls)

    class Meta:
        unique_together = ('city', 'speciality')
