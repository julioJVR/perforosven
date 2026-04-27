from django.db import models
from ventas.models.cotizacion import Cotizacion
from ventas.models.partida_contrato import PartidaContrato


class DetalleCotizacion(models.Model):

    cotizacion = models.ForeignKey(
        Cotizacion, 
        on_delete=models.CASCADE, 
        related_name='detalles'
    )

    partida_contrato = models.ForeignKey(
        PartidaContrato,
        on_delete=models.PROTECT
    )

    descripcion = models.CharField(max_length=255)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=14, decimal_places=2)

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.descripcion} - {self.cotizacion.numero}"
