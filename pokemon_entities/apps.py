from django.apps import AppConfig  # type: ignore


class PokemonEntitiesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pokemon_entities"
    verbose_name = "Покемоны"
