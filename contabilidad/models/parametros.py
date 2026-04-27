from django.db import models




class ParametrosContables(models.Model):
    clave = models.CharField(max_length=60, unique=True)
    valor = models.CharField(max_length=200, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)


class Meta:
    verbose_name = 'Parámetro Contable'
    verbose_name_plural = 'Parámetros Contables'


def __str__(self):
    return f"{self.clave} = {self.valor}"