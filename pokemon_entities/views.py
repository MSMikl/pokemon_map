import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
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
    pokemons = PokemonEntity.objects.filter(appeared_at__lte=timezone.now(), disappeared_at__isnull=True)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons:
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
    pokemons = PokemonEntity.objects.filter(pokemon__id=pokemon_id)
    if not pokemons:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    pokemon = Pokemon.objects.get(id=pokemon_id)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons:
        add_pokemon(
            folium_map, pokemon_entity.lattitude,
            pokemon_entity.longitude,
            request.build_absolute_uri(pokemon.image.url)
        )
    old_style_pokemon = {
            'title_ru':pokemon.title,
            'description':pokemon.description,
            'img_url':request.build_absolute_uri(pokemon.image.url),
            'title_en':pokemon.title_en,
            'title_jp':pokemon.title_jap
    }
    if pokemon.previous_evolution:
        old_style_pokemon['previous_evolution'] = {
            'title':pokemon.previous_evolution.title,
            'pokemon_id':pokemon.previous_evolution.id,
            'img_url':request.build_absolute_uri(
                pokemon
                .previous_evolution
                .image
                .url
            )
        }
    if pokemon.next_evolution.all():
        next_evolution = pokemon.next_evolution.all()[0]
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
