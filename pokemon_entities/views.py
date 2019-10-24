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
    for pokemon_entity in \
            PokemonEntity.objects.prefetch_related('pokemon').all():
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
    requested_pokemon = \
        Pokemon.objects.prefetch_related('pokemon_all_entities').get(id=pokemon_id)

    pokemon_on_page = {
        'pokemon_id': requested_pokemon.id,
        'title_ru': requested_pokemon.title_ru,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description,
        'img_url': make_img_url(requested_pokemon, request),
    }

    try:
        pokemon_previous_evolution = requested_pokemon.previous_evolution
        if pokemon_previous_evolution:
            pokemon_on_page.update({'previous_evolution': {
                'pokemon_id': pokemon_previous_evolution.id,
                'title_ru': pokemon_previous_evolution.title_ru,
                'title_en': pokemon_previous_evolution.title_en,
                'title_jp': pokemon_previous_evolution.title_jp,
                'img_url': make_img_url(pokemon_previous_evolution, request),
            }})

        pokemon_next_evolution = requested_pokemon.next_evolutions.first()
        if pokemon_next_evolution:
            pokemon_on_page.update({'next_evolution': {
                'pokemon_id': pokemon_next_evolution.id,
                'title_ru': pokemon_next_evolution.title_ru,
                'title_en': pokemon_next_evolution.title_en,
                'title_jp': pokemon_next_evolution.title_jp,
                'img_url': make_img_url(pokemon_next_evolution, request),
            }})
    except (IndexError, AttributeError):
        pass

    for pokemon_entity in requested_pokemon.pokemon_all_entities.all():
        img_url = make_img_url(pokemon_entity.pokemon, request)
        add_pokemon(folium_map, pokemon_entity.lat, pokemon_entity.lon,
                    pokemon_entity.pokemon.title_ru, img_url)

    return render(request, "pokemon.html", context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_on_page,
    })
