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
    disappeared_at = models.DateTimeField(default=None, blank=True)
    level = models.IntegerField('Level')
    health = models.IntegerField('Health')
    strength = models.IntegerField('Strength')
    defence = models.IntegerField('Defence')
    stamina = models.IntegerField('Stamina')
    
    
    def __str__(self):
        return '{}, {}'.format(self.lattitude, self.longitude)