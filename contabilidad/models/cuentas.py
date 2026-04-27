# contabilidad/models/cuentas.py
from django.db import models

TIPO_CUENTA_CHOICES = [
    ("ACTIVO", "Activo"),
    ("PASIVO", "Pasivo"),
    ("PATRIMONIO", "Patrimonio"),
    ("INGRESO", "Ingreso"),
    ("COSTO", "Costo"),
    ("GASTO", "Gasto"),
]

NATURALEZA_CHOICES = [
    ("D", "Deudora"),
    ("A", "Acreedora"),
]


class CuentaContable(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CUENTA_CHOICES, default="ACTIVO")
    naturaleza = models.CharField(max_length=1, choices=NATURALEZA_CHOICES, default="D")
    nivel = models.PositiveSmallIntegerField(default=1)
    padre = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="hijas",
    )
    es_activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["codigo"]
        verbose_name = "Cuenta Contable"
        verbose_name_plural = "Cuentas Contables"

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
