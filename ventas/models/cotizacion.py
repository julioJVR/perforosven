from django.db import models
from ventas.models.cliente import Cliente
from ventas.models.contrato import Contrato


class Cotizacion(models.Model):

    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    )

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT, related_name="cotizaciones")

    numero = models.CharField(max_length=50, unique=True)
    fecha = models.DateField()
    fecha_servicio = models.DateField(null=True, blank=True)

    monto_total = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    estado = models.CharField(max_length=15, choices=ESTADOS, default="pendiente")

    def __str__(self):
        return self.numero
