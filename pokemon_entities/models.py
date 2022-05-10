from distutils.command.upload import upload
from django.db import models  # noqa F401
from django.utils import timezone


class Pokemon(models.Model):
    title = models.CharField('Имя покемона', max_length=200)
    title_en = models.CharField('Имя англ.', max_length=200, blank=True)
    title_jap = models.CharField('Имя яп.', max_length=200, blank=True)
    image = models.ImageField(
        'Изображение покемона',
        upload_to='pictures',
        null=True,
        blank=True
    )
    description = models.TextField('Описание', max_length=500, blank=True)
    previous_evolution = models.ForeignKey(
        'Pokemon',
        related_name='next_evolutions',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lattitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')
    appeared_at = models.DateTimeField(
        'Дата и время появления',
        default=timezone.now()
    )
    disappeared_at = models.DateTimeField(
        'Дата и время исчезновения',
        default=None,
        blank=True,
        null=True
    )
    level = models.IntegerField('Уровень', null=True, blank=True)
    health = models.IntegerField('Здоровье', null=True, blank=True)
    strength = models.IntegerField('Сила', null=True, blank=True)
    defence = models.IntegerField('Защита', null=True, blank=True)
    stamina = models.IntegerField('Выносливость', null=True, blank=True)
    
    
    def __str__(self):
        return '{}  {}'.format(self.id, self.pokemon.title)