import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class ComplexPasswordValidator:
    """
    Validador de contraseñas complejas que requiere:
    - Mínimo 8 caracteres
    - Al menos una mayúscula
    - Al menos una minúscula
    - Al menos un número
    - Al menos un carácter especial
    """
    
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                _("La contraseña debe tener al menos 8 caracteres."),
                code='password_too_short',
            )
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos una letra mayúscula."),
                code='password_no_upper',
            )
        
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos una letra minúscula."),
                code='password_no_lower',
            )
        
        if not re.search(r'[0-9]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos un número."),
                code='password_no_digit',
            )
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos un carácter especial (!@#$%^&*(),.?\":{}|<>_-+=[]\\/)."),
                code='password_no_special',
            )
    
    def get_help_text(self):
        return _(
            "Tu contraseña debe tener al menos 8 caracteres, "
            "incluir mayúsculas, minúsculas, números y caracteres especiales."
        )


class NoCommonPasswordValidator:
    """
    Valida que la contraseña no sea una de las más comunes
    """
    
    COMMON_PASSWORDS = [
        'password', '12345678', 'qwerty', 'abc123', 'password123',
        'admin', 'letmein', 'welcome', 'monkey', '1234567890',
        'admin123', 'root', 'toor', 'pass', 'test', 'guest',
        'administrador', 'usuario', 'contraseña', '123456789'
    ]
    
    def validate(self, password, user=None):
        if password.lower() in self.COMMON_PASSWORDS:
            raise ValidationError(
                _("Esta contraseña es demasiado común. Por favor elige otra."),
                code='password_too_common',
            )
    
    def get_help_text(self):
        return _("Tu contraseña no puede ser una contraseña comúnmente usada.")


class NoUserAttributeSimilarityValidator:
    """
    Valida que la contraseña no sea similar al nombre de usuario o email
    """
    
    def validate(self, password, user=None):
        if not user:
            return
        
        # Verificar username
        if user.username and user.username.lower() in password.lower():
            raise ValidationError(
                _("La contraseña no puede contener tu nombre de usuario."),
                code='password_contains_username',
            )
        
        # Verificar email
        if user.email:
            email_name = user.email.split('@')[0]
            if email_name.lower() in password.lower():
                raise ValidationError(
                    _("La contraseña no puede contener tu email."),
                    code='password_contains_email',
                )
        
        # Verificar nombre
        if user.first_name and len(user.first_name) > 3:
            if user.first_name.lower() in password.lower():
                raise ValidationError(
                    _("La contraseña no puede contener tu nombre."),
                    code='password_contains_name',
                )
        
        # Verificar apellido
        if user.last_name and len(user.last_name) > 3:
            if user.last_name.lower() in password.lower():
                raise ValidationError(
                    _("La contraseña no puede contener tu apellido."),
                    code='password_contains_lastname',
                )
    
    def get_help_text(self):
        return _("Tu contraseña no puede ser similar a tu información personal.")