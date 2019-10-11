from django.db import models


class Pokemon(models.Model):
    img_file = models.ImageField(verbose_name='изображение')
    title_ru = models.CharField(verbose_name='наименование рус', null=False,
                                max_length=200)
    title_en = models.CharField(verbose_name='наименование англ', blank=True,
                                null=False, max_length=200)
    title_jp = models.CharField(verbose_name='наименование яп', blank=True,
                                null=False, max_length=200)
    description = models.TextField(verbose_name='описание', max_length=10000,
                                   blank=True, null=False)
    previous_evolution = models.ForeignKey('self', blank=True, null=True,
                                           on_delete=models.SET_NULL,
										   related_name='next_evolutions',
                                           verbose_name='Из кого эволюционировал')
    
    #next_evolution = models.ForeignKey('self', blank=True, null=True,
     #                                  related_name='+', on_delete=models.SET_NULL,
     #                                  verbose_name='В кого эволюционирует')

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, verbose_name='покемон',
                                on_delete=models.CASCADE)
    lat = models.FloatField(verbose_name='широта')
    lon = models.FloatField(verbose_name='долгота')
    appeared_at = models.DateTimeField(verbose_name='время появления',
                                       default=None, blank=True, null=True)
    disappeared_at = models.DateTimeField(verbose_name='время исчезания',
                                          default=None, blank=True, null=True)

    level = models.IntegerField(verbose_name='уровень', default=0, blank=True)
    health = models.IntegerField(verbose_name='здоровье', default=0, blank=True)
    strength = models.IntegerField(verbose_name='сила', default=0, blank=True)
    defence = models.IntegerField(verbose_name='защита', default=0, blank=True)
    stamina = models.IntegerField(verbose_name='выносливость', default=0,
                                  blank=True)


    def __str__(self):
        return f'покемон - {self.pokemon} широта: {self.lat}, долгота{self.lon}'
