# Contabilidad (módulo) — Instalación y notas

## Resumen
Módulo contable modular (submódulos en `models/`) con:
- Cuentas contables (CRUD)
- Asientos y movimientos contables (CRUD básico)
- Importador de plan de cuentas desde Excel (pandas/openpyxl)
- Dashboard básico + reportes placeholder

## Requisitos
- Python 3.10+ (probado con 3.11/3.13)
- Django 4.x / 5.x (ajusta según tu proyecto). Tu proyecto parece usar Django 5.2.x
- pandas (opcional para importar Excel). Si no, usa openpyxl
- openpyxl

Instalación de dependencias:
```bash
pip install django openpyxl pandas
