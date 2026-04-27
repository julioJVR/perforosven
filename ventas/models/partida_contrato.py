from django.db import models
from .contrato import Contrato


class PartidaContrato(models.Model):
    contrato = models.ForeignKey(
        Contrato,
        on_delete=models.CASCADE,
        related_name="partidas"
    )
    descripcion = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.descripcion} ({self.contrato.numero})"
