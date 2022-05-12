import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.utils import timezone

from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemon_entites = PokemonEntity.objects.filter(
        appeared_at__lte=timezone.now(),
        disappeared_at__isnull=True
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entites:
        add_pokemon(
            folium_map, pokemon_entity.lattitude,
            pokemon_entity.longitude,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )
    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon_to_show = get_object_or_404(Pokemon, id=pokemon_id)
    pokemon_entities = get_list_or_404(PokemonEntity, pokemon__id=pokemon_id)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lattitude,
            pokemon_entity.longitude,
            request.build_absolute_uri(pokemon_to_show.image.url)
        )
    old_style_pokemon = {
            'title_ru':pokemon_to_show.title,
            'description':pokemon_to_show.description,
            'img_url':request.build_absolute_uri(pokemon_to_show.image.url),
            'title_en':pokemon_to_show.title_en,
            'title_jp':pokemon_to_show.title_jap
    }
    if pokemon_to_show.previous_evolution:
        old_style_pokemon['previous_evolution'] = {
            'title':pokemon_to_show.previous_evolution.title,
            'pokemon_id':pokemon_to_show.previous_evolution.id,
            'img_url':request.build_absolute_uri(
                pokemon_to_show
                .previous_evolution
                .image
                .url
            )
        }
    next_evolution = pokemon_to_show.next_evolutions.all().first()
    if next_evolution:
        old_style_pokemon['next_evolution'] = {
            'title':next_evolution.title,
            'pokemon_id':next_evolution.id,
            'img_url':request.build_absolute_uri(
                next_evolution
                .image
                .url
            )
        }
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon':old_style_pokemon
        }
    )
