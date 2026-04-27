# compras/models.py
from django.db import models
from django.core.validators import RegexValidator, EmailValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.utils import timezone

# =============================
# MODELO PROVEEDOR
# =============================
class Proveedor(models.Model):
    codigo_proveedor = models.CharField(max_length=20, unique=True, default='P0001')
    rif = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="RIF",
        validators=[RegexValidator(r'^[JGVEP]-\d{8}-\d$', 'Formato inválido. Ej: J-12345678-9')]
    )
    nombre_empresa = models.CharField(max_length=255, verbose_name="Nombre o Razón Social")
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True, validators=[EmailValidator()])
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    representante_nombre = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre del Representante")
    representante_cedula = models.CharField(max_length=20, blank=True, null=True, verbose_name="Cédula del Representante")
    representante_telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono del Representante")
    representante_correo = models.EmailField(blank=True, null=True, verbose_name="Correo del Representante")

    banco_nacional = models.CharField(max_length=100, blank=True, null=True, verbose_name="Banco Nacional")
    cuenta_nacional = models.CharField(max_length=30, blank=True, null=True, verbose_name="Cuenta Nacional")
    tipo_cuenta_nacional = models.CharField(
        max_length=20,
        choices=[('corriente', 'Corriente'), ('ahorro', 'Ahorro')],
        blank=True, null=True
    )

    banco_extranjero = models.CharField(max_length=100, blank=True, null=True, verbose_name="Banco Extranjero")
    cuenta_extranjera = models.CharField(max_length=30, blank=True, null=True, verbose_name="Cuenta Extranjera")
    swift = models.CharField(max_length=20, blank=True, null=True, verbose_name="Código SWIFT")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['nombre_empresa']

    def __str__(self):
        return f"{self.codigo_proveedor} - {self.nombre_empresa} ({self.rif})"

    def save(self, *args, **kwargs):
        if not self.codigo_proveedor:
            last = Proveedor.objects.order_by('-id').first()
            next_id = (last.id + 1) if last else 1
            self.codigo_proveedor = f"PRV-{next_id:04d}"
        super().save(*args, **kwargs)


# =============================
# MODELO PRODUCTO
# =============================
class Producto(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=200)
    unidad_medida = models.CharField(max_length=20)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['descripcion']

    def __str__(self):
        return f"{self.descripcion} ({self.codigo})"


# =============================
# MODELO ORDEN DE COMPRA
# =============================
class OrdenCompra(models.Model):
    numero_oc = models.CharField(max_length=20, unique=True, verbose_name="Número de Orden de Compra")
    fecha = models.DateField(auto_now_add=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Orden de Compra"
        verbose_name_plural = "Órdenes de Compra"
        ordering = ['-fecha']

    def __str__(self):
        return f"OC-{self.numero_oc} - {self.proveedor.nombre_empresa}"

    def save(self, *args, **kwargs):
        if not self.numero_oc:
            last = OrdenCompra.objects.order_by('-id').first()
            next_id = (last.id + 1) if last else 1
            self.numero_oc = f"{next_id:05d}"
        super().save(*args, **kwargs)


# =============================
# MODELO DETALLE ORDEN
# =============================
class DetalleOrden(models.Model):
    orden = models.ForeignKey('OrdenCompra', on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('Producto', on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Detalle de Orden'
        verbose_name_plural = 'Detalles de Órdenes'

    def __str__(self):
        return f"{self.producto.descripcion} ({self.cantidad})"

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario


# =============================
# MODELO FACTURA
# =============================
class Factura(models.Model):
    MONEDAS = [('USD', 'Dólares (USD)'), ('VES', 'Bolívares (VES)')]

    proveedor = models.ForeignKey('Proveedor', on_delete=models.PROTECT)
    orden_compra = models.ForeignKey('OrdenCompra', on_delete=models.SET_NULL, null=True, blank=True)
    fecha_factura = models.DateField()
    fecha_registro = models.DateTimeField(default=timezone.now)
    descripcion_servicio = models.TextField()
    numero_factura = models.CharField(max_length=50, unique=True)
    numero_control = models.CharField(max_length=50, blank=True, null=True)
    soporte_documento = models.TextField(blank=True, null=True)
    moneda = models.CharField(max_length=3, choices=MONEDAS, default='VES')
    monto_base = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    iva = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    total_factura = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    municipio = models.CharField(max_length=100)
    ret_iva = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    ret_islr = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    tasa_cambio = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1.00'))

    # NUEVOS CAMPOS
    tiene_iva = models.BooleanField(default=False)
    alicuota_iva = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # Retención municipal: porcentaje y monto
    porcentaje_ret_municipal = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))],
        verbose_name="Porcentaje Retención Municipal (%)"
    )
    ret_municipal = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal('0.00'),
        verbose_name="Monto Retención Municipal"
    )

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        ordering = ['-fecha_factura']

    def clean(self):
        if self.monto_base <= 0:
            raise ValidationError("El monto base debe ser mayor que cero.")
        if self.porcentaje_ret_municipal < 0 or self.porcentaje_ret_municipal > 100:
            raise ValidationError("El porcentaje de retención municipal debe estar entre 0 y 100.")

    def save(self, *args, **kwargs):
        # Validar antes
        self.full_clean()

        base_en_bs = (self.monto_base * self.tasa_cambio) if self.moneda == 'USD' else self.monto_base

        # Si iva es 0, se asume que debe calcularse (puede ser sobreescrito por la vista)
        try:
            # si self.iva ya tiene valor mayor que 0, no lo sobreescribimos
            if not self.iva or Decimal(self.iva) == Decimal('0.00'):
                self.iva = (base_en_bs * Decimal('0.16')).quantize(Decimal('0.01'))
        except Exception:
            self.iva = (base_en_bs * Decimal('0.16')).quantize(Decimal('0.01'))

        self.total_factura = (base_en_bs + self.iva).quantize(Decimal('0.01'))
        self.ret_municipal = (base_en_bs * (self.porcentaje_ret_municipal / Decimal('100.00'))).quantize(Decimal('0.01'))

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Factura {self.numero_factura} - {self.proveedor.nombre_empresa}"

