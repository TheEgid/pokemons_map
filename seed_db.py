import argparse
import io
import os
import random
import sys
from pathlib import Path

import django
import requests
from django.core.files.base import ContentFile
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pogomap.settings")
django.setup()

from pokemon_entities.models import Pokemon, PokemonEntity

POKEMONS: list[dict[str, str]] = [
    {
        "id": "1",
        "name": "Bulbasaur",
        "title_ru": "Бульбазавр",
        "title_jp": "フシギダネ",
        "description": "Начальный покемон травяного типа. Имеет семя на спине.",
    },
    {
        "id": "4",
        "name": "Charmander",
        "title_ru": "Чармандер",
        "title_jp": "ヒトカゲ",
        "description": "Огненный покемон. Пламя на хвосте указывает на его здоровье.",
    },
    {
        "id": "7",
        "name": "Squirtle",
        "title_ru": "Сквиртл",
        "title_jp": "ゼニガメ",
        "description": "Водяной покемон. Атакует водой изо рта.",
    },
    {
        "id": "25",
        "name": "Pikachu",
        "title_ru": "Пикачу",
        "title_jp": "ピカチュウ",
        "description": "Электрический покемон. Хранит электричество в щеках.",
    },
    {
        "id": "39",
        "name": "Jigglypuff",
        "title_ru": "Джигглипуфф",
        "title_jp": "プリン",
        "description": "Поющий покемон. Усыпляет врагов своей мелодией.",
    },
    {
        "id": "52",
        "name": "Meowth",
        "title_ru": "Мяут",
        "title_jp": "ニャース",
        "description": "Кошак-воришка. Обожает блестящие предметы.",
    },
    {
        "id": "54",
        "name": "Psyduck",
        "title_ru": "Псайдак",
        "title_jp": "コダック",
        "description": "Водный покемон. Страдает от головной боли.",
    },
    {
        "id": "63",
        "name": "Abra",
        "title_ru": "Абра",
        "title_jp": "ケーシィ",
        "description": "Телепатический покемон. Спит 18 часов в сутки.",
    },
    {
        "id": "74",
        "name": "Geodude",
        "title_ru": "Грув",
        "title_jp": "イシツブテ",
        "description": "Каменный покемон. Часто встречается на горных тропах.",
    },
    {
        "id": "92",
        "name": "Gastly",
        "title_ru": "Гастли",
        "title_jp": "ユンゲラー",
        "description": "Призрачный покемон. Состоит из газа.",
    },
]

POKEMON_URL_TEMPLATE: str = (
    "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png"
)

MOSCOW_CENTER: tuple[float, float] = (55.751244, 37.618423)
SPREAD: float = 0.1


def download_pokemon_image(pokemon_id: str) -> ContentFile | None:
    url = POKEMON_URL_TEMPLATE.format(id=pokemon_id)
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            img = Image.open(io.BytesIO(response.content)).convert("RGBA")
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            return ContentFile(buffer.read(), name=f"{pokemon_id}.png")
    except (OSError, requests.RequestException) as e:
        print(f"Failed to download image for pokemon {pokemon_id}: {e}")
    return None


def seed_pokemons(count: int = 10) -> list[Pokemon]:
    pokemons: list[Pokemon] = []
    for pokemon_data in POKEMONS[:count]:
        img = download_pokemon_image(pokemon_data["id"])
        if img is None:
            print(f"Skipping {pokemon_data['title_ru']} due to image download failure")
            continue

        pokemon = Pokemon.objects.create(
            img_file=img,
            title_ru=pokemon_data["title_ru"],
            title_en=pokemon_data["name"],
            title_jp=pokemon_data["title_jp"],
            description=pokemon_data["description"],
        )
        pokemons.append(pokemon)
        print(f"Создан покемон: {pokemon.title_ru} ({pokemon.title_en})")
    return pokemons


def seed_evolutions(pokemons: list[Pokemon]) -> None:
    evolution_chains: list[tuple[int, ...]] = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (9,),
    ]
    for chain in evolution_chains:
        if chain[0] >= len(pokemons):
            continue
        for i in range(len(chain) - 1):
            if chain[i] < len(pokemons) and chain[i + 1] < len(pokemons):
                pokemons[chain[i + 1]].previous_evolution = pokemons[chain[i]]
                pokemons[chain[i + 1]].save(update_fields=["previous_evolution"])
                print(
                    f"Эволюция: {pokemons[chain[i]].title_ru} -> {pokemons[chain[i + 1]].title_ru}"
                )


def seed_entities(pokemons: list[Pokemon], count_per_pokemon: int = 5) -> int:
    total: int = 0
    for pokemon in pokemons:
        for _ in range(count_per_pokemon):
            lat = MOSCOW_CENTER[0] + random.uniform(-SPREAD, SPREAD)
            lon = MOSCOW_CENTER[1] + random.uniform(-SPREAD, SPREAD)
            PokemonEntity.objects.create(
                pokemon=pokemon,
                lat=round(lat, 6),
                lon=round(lon, 6),
            )
            total += 1
        print(f"Добавлено {count_per_pokemon} сущностей для {pokemon.title_ru}")
    return total


def main(count: int = 10) -> None:
    print("Удаление существующих данных...")
    PokemonEntity.objects.all().delete()
    Pokemon.objects.all().delete()

    print(f"\nСоздание {count} покемонов...")
    pokemons = seed_pokemons(count)

    print("\nНастройка эволюций...")
    seed_evolutions(pokemons)

    print("\nДобавление сущностей на карту...")
    total = seed_entities(pokemons)

    print(f"\nГотово! Создано {len(pokemons)} покемонов и {total} сущностей на карте.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Заполнение базы данных покемонами")
    parser.add_argument(
        "count",
        type=int,
        nargs="?",
        default=10,
        help="Количество покемонов (по умолчанию 10)",
    )
    args = parser.parse_args()
    main(args.count)
