from django.contrib import admin # pyright: ignore[reportMissingModuleSource]

from .models import Pokemon, PokemonEntity


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ["id", "title_ru", "title_en", "title_jp", "previous_evolution"]
    search_fields = ["title_ru", "title_en", "title_jp"]
    list_filter = ["previous_evolution"]


@admin.register(PokemonEntity)
class PokemonEntityAdmin(admin.ModelAdmin):
    list_display = ["id", "pokemon", "lat", "lon", "appeared_at", "disappeared_at"]
    list_filter = ["pokemon", "appeared_at", "disappeared_at"]
    search_fields = ["pokemon__title_ru"]
    list_select_related = ["pokemon"]
