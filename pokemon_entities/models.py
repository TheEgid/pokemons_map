from django.db import models


class Pokemon(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    title_ru = models.CharField(max_length=200)
    img_url = models.ImageField('изображение', blank=True, null=True)
    # img_url = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    appeared_at = models.DateTimeField(default=None, blank=True, null=True)
    disappeared_at = models.DateTimeField(default=None, blank=True, null=True)

    level = models.IntegerField(default=0, blank=True)
    health = models.IntegerField(default=0, blank=True)
    strength = models.IntegerField(default=0, blank=True)
    defence = models.IntegerField(default=0, blank=True)
    stamina = models.IntegerField(default=0, blank=True)

    pokemon = models.ForeignKey(Pokemon, default=None,
                                on_delete=models.CASCADE)

    def __str__(self):
        return f'pokemon - {self.pokemon} latitude: {self.lat}, longitude{self.lon}'
