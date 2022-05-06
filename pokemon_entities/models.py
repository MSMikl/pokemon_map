from django.db import models  # noqa F401

class Pokemon(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField('Имя покемона', max_length=200)
    
    def __str__(self):
        return self.title
