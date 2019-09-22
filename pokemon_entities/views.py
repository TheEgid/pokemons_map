import folium
import os
from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def make_image_url(pokemon, request):
    return request.build_absolute_uri(pokemon.img_url.url)


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
        img_url = make_image_url(pokemon_entity.pokemon, request)
        add_pokemon(folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon_entity.pokemon.title_ru, img_url)

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'title_ru': pokemon.title_ru,
            'img_url': pokemon.img_url,
        })


    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=10)

    for pokemon in Pokemon.objects.all():
        if pokemon.id == int(pokemon_id):
            requested_pokemon = pokemon
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    for pokemon_entity in PokemonEntity.objects.filter(pokemon_id=requested_pokemon.id):
        img_url = make_image_url(requested_pokemon, request)
        add_pokemon(folium_map, pokemon_entity.lat, pokemon_entity.lon,
                    requested_pokemon.title_ru, img_url)

    return render(request, "pokemon.html", context={
        'map': folium_map._repr_html_(),
        'pokemon': requested_pokemon
    })
