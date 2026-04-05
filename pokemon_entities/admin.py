from typing import ClassVar

from django.contrib import admin  # type: ignore[reportMissingModuleSource]

from .models import Pokemon, PokemonEntity


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display: ClassVar[list[str]] = [
        "id",
        "title_ru",
        "title_en",
        "title_jp",
        "previous_evolution",
    ]
    search_fields: ClassVar[list[str]] = ["title_ru", "title_en", "title_jp"]
    list_filter: ClassVar[list[str]] = ["previous_evolution"]


@admin.register(PokemonEntity)
class PokemonEntityAdmin(admin.ModelAdmin):
    list_display: ClassVar[list[str]] = [
        "id",
        "pokemon",
        "lat",
        "lon",
        "appeared_at",
        "disappeared_at",
    ]
    list_filter: ClassVar[list[str]] = ["pokemon", "appeared_at", "disappeared_at"]
    search_fields: ClassVar[list[str]] = ["pokemon__title_ru"]
    list_select_related: ClassVar[list[str]] = ["pokemon"]
