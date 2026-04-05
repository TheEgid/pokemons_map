from dataclasses import dataclass
from typing import TYPE_CHECKING

import folium  # type: ignore[reportMissingImports]
from branca.element import Element

if TYPE_CHECKING:
    from django.http import HttpRequest  # type: ignore

    from .models import Pokemon, PokemonEntity


MOSCOW_CENTER: tuple[float, float] = (55.751244, 37.618423)
DEFAULT_IMAGE_URL: str = (
    "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/!:.png/revision/latest"
    "/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"
)


@dataclass(frozen=True)
class MapMarker:
    lat: float
    lon: float
    name: str
    image_url: str

    def add_to_map(self, folium_map: folium.Map) -> None:
        icon = folium.features.CustomIcon(self.image_url, icon_size=(50, 50))
        folium.Marker(
            location=[self.lat, self.lon],
            tooltip=self.name,
            icon=icon,
        ).add_to(folium_map)


def build_map(*markers: MapMarker) -> folium.Map:
    result = folium.Map(
        location=MOSCOW_CENTER,
        zoom_start=12,
        tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        attr=" ",
    )

    # Hide attribution via Branca Element injection
    try:
        style = Element(
            "<style>.leaflet-control-attribution { display: none !important; }</style>"
        )
        result.get_root().html.add_child(style)
    except Exception:
        pass

    for marker in markers:
        marker.add_to_map(result)

    return result


def make_img_url(pokemon: "Pokemon", request: "HttpRequest") -> str:
    return request.build_absolute_uri(pokemon.img_file.url)


def create_pokemon_markers(
    entities: list["PokemonEntity"],
    request: "HttpRequest",
) -> list[MapMarker]:
    return [
        MapMarker(
            lat=entity.lat,
            lon=entity.lon,
            name=entity.pokemon.title_ru,
            image_url=make_img_url(entity.pokemon, request),
        )
        for entity in entities
    ]
