from django.db import models
from django.utils import timezone
# import local CuentaContable (no circular if cuentas.py doesn't import asiento)
from .cuentas import CuentaContable

class AsientoContable(models.Model):
    numero = models.CharField(max_length=20, unique=True, verbose_name="Número de Asiento")
    descripcion = models.CharField(max_length=255, verbose_name="Descripción")
    fecha = models.DateField(default=timezone.now)
    creado_en = models.DateTimeField(auto_now_add=True)

    total_debe = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_haber = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Asiento Contable"
        verbose_name_plural = "Asientos Contables"
        ordering = ["-fecha", "-numero"]

    def __str__(self):
        return f"Asiento #{self.numero} - {self.descripcion}"

    def actualizar_totales(self):
        movimientos = self.lineas.all()
        debe = sum([m.debe for m in movimientos]) if movimientos else 0
        haber = sum([m.haber for m in movimientos]) if movimientos else 0
        self.total_debe = debe
        self.total_haber = haber
        self.save(update_fields=["total_debe", "total_haber"])

    def esta_cuadrado(self):
        return (self.total_debe or 0) == (self.total_haber or 0)

class MovimientoContable(models.Model):
    asiento = models.ForeignKey(
        AsientoContable,
        related_name="lineas",
        on_delete=models.CASCADE
    )
    cuenta = models.ForeignKey(
        CuentaContable,
        on_delete=models.PROTECT,
        verbose_name="Cuenta Contable"
    )
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    debe = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    haber = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Movimiento Contable"
        verbose_name_plural = "Movimientos Contables"
        ordering = ["id"]

    def __str__(self):
        tipo = "Debe" if self.debe > 0 else "Haber"
        valor = self.debe if self.debe > 0 else self.haber
        return f"{self.cuenta.codigo} - {self.cuenta.nombre} ({tipo}: {valor})"
