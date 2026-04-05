from pydantic import BaseModel, ConfigDict


class EvolutionInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pokemon_id: int
    title_ru: str
    title_en: str = ""
    title_jp: str = ""
    img_url: str


class PokemonBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pokemon_id: int
    title_ru: str
    img_url: str


class PokemonDetail(PokemonBase):
    title_en: str = ""
    title_jp: str = ""
    description: str = ""
    previous_evolution: EvolutionInfo | None = None
    next_evolution: EvolutionInfo | None = None


class PokemonEntityData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    lat: float
    lon: float
    pokemon_name: str
    img_url: str


class MapContext(BaseModel):
    map_html: str
    pokemons: list[PokemonBase] = []
    pokemon: PokemonDetail | None = None
