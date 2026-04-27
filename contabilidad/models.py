# contabilidad/models.py
from django.db import models
from django.utils import timezone

TIPO_CUENTA_CHOICES = [
    ('ACTIVO', 'Activo'),
    ('PASIVO', 'Pasivo'),
    ('PATRIMONIO', 'Patrimonio'),
    ('INGRESO', 'Ingreso'),
    ('COSTO', 'Costo'),
    ('GASTO', 'Gasto'),
]

NATURALEZA_CHOICES = (
    ('D', 'Deudora'),
    ('A', 'Acreedora'),
)


class CuentaContable(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)

    tipo = models.CharField(max_length=20, choices=TIPO_CUENTA_CHOICES, default='ACTIVO')
    naturaleza = models.CharField(max_length=1, choices=NATURALEZA_CHOICES, default='D')

    nivel = models.PositiveSmallIntegerField(default=1)
    padre = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='hijas')

    es_activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['codigo']
        verbose_name = 'Cuenta Contable'
        verbose_name_plural = 'Cuentas Contables'

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    

class AsientoContable(models.Model):
    numero = models.CharField(max_length=20, unique=True, verbose_name="Número de Asiento")
    descripcion = models.CharField(max_length=255)
    fecha = models.DateField(default=timezone.now)
    creado_en = models.DateTimeField(auto_now_add=True)

    total_debe = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_haber = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Asiento Contable"
        verbose_name_plural = "Asientos Contables"
        ordering = ["-fecha", "-numero"]

    def __str__(self):
        return f"Asiento #{self.numero}"

    def actualizar_totales(self):
        movimientos = self.lineas.all()
        self.total_debe = sum([m.debe for m in movimientos])
        self.total_haber = sum([m.haber for m in movimientos])
        self.save(update_fields=["total_debe", "total_haber"])

    def esta_cuadrado(self):
        return self.total_debe == self.total_haber
        

class MovimientoContable(models.Model):
    asiento = models.ForeignKey(
        AsientoContable,
        related_name="lineas",
        on_delete=models.CASCADE
    )
    cuenta = models.ForeignKey(CuentaContable, on_delete=models.PROTECT)

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
