from distutils.command.upload import upload
from django.db import models  # noqa F401
from django.utils import timezone

class Pokemon(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField('Имя покемона', max_length=200)
    image = models.ImageField('Изображение покемона', upload_to='pictures', null=True, blank=True)
    
    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lattitude = models.FloatField('Lat.')
    longitude = models.FloatField('Lon.')
    appeared_at = models.DateTimeField(default=timezone.now())
    disappeared_at = models.DateTimeField(default=None, blank=True, null=True)
    level = models.IntegerField('Level', null=True, blank=True)
    health = models.IntegerField('Health', null=True, blank=True)
    strength = models.IntegerField('Strength', null=True, blank=True)
    defence = models.IntegerField('Defence', null=True, blank=True)
    stamina = models.IntegerField('Stamina', null=True, blank=True)
    
    
    def __str__(self):
        return '{}  {}'.format(self.id, self.pokemon.title)