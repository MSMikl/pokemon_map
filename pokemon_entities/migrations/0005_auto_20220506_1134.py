# Generated by Django 3.1.14 on 2022-05-06 08:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0004_pokemonentity_pokemon'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemonentity',
            name='appeared_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 6, 8, 34, 22, 144587, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='pokemonentity',
            name='disappeared_at',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
