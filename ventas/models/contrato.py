from django.db import models
from ventas.models.cliente import Cliente


class Contrato(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="contratos")

    numero = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)

    monto_total = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.numero} - {self.cliente.nombre}"


