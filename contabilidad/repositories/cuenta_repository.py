from contabilidad.models import CuentaContable


class CuentaRepository:

    @staticmethod
    def get_by_codigo(codigo: str):
        return CuentaContable.objects.filter(codigo=codigo).first()

    @staticmethod
    def all():
        return CuentaContable.objects.all()

    @staticmethod
    def create(**kwargs):
        return CuentaContable.objects.create(**kwargs)
