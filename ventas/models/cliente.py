from django.db import models

class Cliente(models.Model):
    TIPO_DOCUMENTO = (
        ('J', 'Jurídico'),
        ('V', 'Natural'),
        ('E', 'Extranjero'),
    )

    tipo_documento = models.CharField(max_length=1, choices=TIPO_DOCUMENTO)
    rif = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=150)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.tipo_documento}-{self.rif} {self.nombre}"
