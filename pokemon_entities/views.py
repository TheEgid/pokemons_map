from typing import Annotated

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.http import require_http_methods

from .models import Pokemon, PokemonEntity
from .schemas import EvolutionInfo, MapContext, PokemonBase, PokemonDetail
from .services import build_map, create_pokemon_markers, make_img_url


@require_http_methods(["GET"])
def index(request: HttpRequest) -> HttpResponse:
    entities = list(PokemonEntity.objects.select_related("pokemon").all())
    markers = create_pokemon_markers(entities, request)
    folium_map = build_map(*markers)

    pokemons = [
        PokemonBase(
            pokemon_id=p.id,
            title_ru=p.title_ru,
            img_url=p.img_file.url,
        )
        for p in Pokemon.objects.only("id", "title_ru", "img_file")
    ]

    context = MapContext(map_html=folium_map._repr_html_(), pokemons=pokemons)
    return render(request, "mainpage.html", context={"map": context.map_html, "pokemons": context.pokemons})


@require_http_methods(["GET"])
def pokemon_detail(request: HttpRequest, pokemon_id: int) -> HttpResponse:
    pokemon = (
        Pokemon.objects.prefetch_related("pokemon_all_entities", "next_evolutions")
        .select_related("previous_evolution")
        .get(id=pokemon_id)
    )

    entities = list(pokemon.pokemon_all_entities.all())
    markers = create_pokemon_markers(entities, request)
    folium_map = build_map(*markers)

    prev = None
    if pokemon.previous_evolution:
        prev = EvolutionInfo(
            pokemon_id=pokemon.previous_evolution.id,
            title_ru=pokemon.previous_evolution.title_ru,
            title_en=pokemon.previous_evolution.title_en,
            title_jp=pokemon.previous_evolution.title_jp,
            img_url=make_img_url(pokemon.previous_evolution, request),
        )

    next_evo = pokemon.next_evolutions.first()
    next_evo_data = None
    if next_evo:
        next_evo_data = EvolutionInfo(
            pokemon_id=next_evo.id,
            title_ru=next_evo.title_ru,
            title_en=next_evo.title_en,
            title_jp=next_evo.title_jp,
            img_url=make_img_url(next_evo, request),
        )

    pokemon_detail = PokemonDetail(
        pokemon_id=pokemon.id,
        title_ru=pokemon.title_ru,
        title_en=pokemon.title_en,
        title_jp=pokemon.title_jp,
        description=pokemon.description,
        img_url=make_img_url(pokemon, request),
        previous_evolution=prev,
        next_evolution=next_evo_data,
    )

    return render(
        request,
        "pokemon.html",
        context={"map": folium_map._repr_html_(), "pokemon": pokemon_detail},
    )
