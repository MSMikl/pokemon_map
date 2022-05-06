from distutils.command.upload import upload
from django.db import models  # noqa F401

class Pokemon(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField('Имя покемона', max_length=200)
    image = models.ImageField('Изображение покемона', upload_to='pictures', null=True, blank=True)
    
    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    lattitude = models.FloatField('Lat.')
    longitude = models.FloatField('Lon.')
    
    def __str__(self):
        return '{}, {}'.format(self.lattitude, self.longitude)