from django.db import models # type: ignore


class Pokemon(models.Model):
    img_file = models.ImageField(upload_to="pokemons/")
    title_ru = models.CharField(max_length=200, verbose_name="наименование рус")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="наименование англ")
    title_jp = models.CharField(max_length=200, blank=True, verbose_name="наименование яп")
    description = models.TextField(max_length=10000, blank=True, verbose_name="описание")
    previous_evolution = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="next_evolutions",
        verbose_name="Из кого эволюционировал",
    )

    class Meta:
        verbose_name = "Покемон"
        verbose_name_plural = "Покемоны"

    def __str__(self) -> str:
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name="pokemon_all_entities",
        verbose_name="покемон",
    )
    lat = models.FloatField(verbose_name="широта")
    lon = models.FloatField(verbose_name="долгота")
    appeared_at = models.DateTimeField(blank=True, null=True, verbose_name="время появления")
    disappeared_at = models.DateTimeField(blank=True, null=True, verbose_name="время исчезания")
    level = models.IntegerField(default=0, blank=True, verbose_name="уровень")
    health = models.IntegerField(default=0, blank=True, verbose_name="здоровье")
    strength = models.IntegerField(default=0, blank=True, verbose_name="сила")
    defence = models.IntegerField(default=0, blank=True, verbose_name="защита")
    stamina = models.IntegerField(default=0, blank=True, verbose_name="выносливость")

    class Meta:
        verbose_name = "Сущность покемона"
        verbose_name_plural = "Сущности покемонов"
        indexes = [
            models.Index(fields=["lat", "lon"]),
            models.Index(fields=["appeared_at"]),
        ]

    def __str__(self) -> str:
        return f"покемон - {self.pokemon} широта: {self.lat}, долгота: {self.lon}"
