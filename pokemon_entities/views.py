import folium
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def make_img_url(pokemon, request):
    return request.build_absolute_uri(pokemon.img_file.url)


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=10)
    for pokemon_entity in PokemonEntity.objects.all():
        img_url = make_img_url(pokemon_entity.pokemon, request)
        add_pokemon(folium_map, pokemon_entity.lat, pokemon_entity.lon,
                    pokemon_entity.pokemon.title_ru, img_url)

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'title_ru': pokemon.title_ru,
            'img_url': pokemon.img_file.url,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=10)
    requested_pokemon = get_object_or_404(Pokemon, pk=int(pokemon_id))
    requested_pokemon.img_url = make_img_url(requested_pokemon, request)
    pokemon_previous_evolution = requested_pokemon.previous_evolution

    try:
        requested_pokemon.previous_evolution.pokemon_id = \
            pokemon_previous_evolution.id
        requested_pokemon.previous_evolution.img_url = make_img_url(
            pokemon_previous_evolution, request)
    except AttributeError:
        requested_pokemon.previous_evolution = None

    try:
        pokemon_next_evolution = requested_pokemon.next_evolutions.all()[0]
        setattr(requested_pokemon, 'next_evolution', pokemon_next_evolution)
        requested_pokemon.next_evolution.pokemon_id = \
            pokemon_next_evolution.id
        requested_pokemon.next_evolution.img_url = make_img_url(
            pokemon_next_evolution, request)
    except (IndexError, AttributeError):
        requested_pokemon.next_evolution = None

    for pokemon_entity in requested_pokemon.pokemon_all_entities.all():
        img_url = make_img_url(pokemon_entity.pokemon, request)
        add_pokemon(folium_map, pokemon_entity.lat, pokemon_entity.lon,
                    pokemon_entity.pokemon.title_ru, img_url)

    return render(request, "pokemon.html", context={
        'map': folium_map._repr_html_(),
        'pokemon': requested_pokemon
    })
