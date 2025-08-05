# Base_App/encryption.py
import base64
from cryptography.fernet import Fernet
from django.conf import settings
from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.core.validators import ValidationError

class EncryptedFieldMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._encryption_key = getattr(settings, 'FIELD_ENCRYPTION_KEY', None)
        if not self._encryption_key:
            raise ImproperlyConfigured(
                'FIELD_ENCRYPTION_KEY must be set in settings for encrypted fields'
            )
        self._fernet = Fernet(self._encryption_key)

    def _is_encrypted(self, value):
        if not isinstance(value, str):
            return False
        try:
            encrypted_data = base64.b64decode(value.encode('utf-8'))
            self._fernet.decrypt(encrypted_data)
            return True
        except Exception:
            return False

    def _is_valid_base64(self, value):
        if not isinstance(value, str):
            return False
        try:
            base64.b64decode(value.encode('utf-8'))
            return True
        except Exception:
            return False

    def get_prep_value(self, value):
        if value is None:
            return None
        if self._is_encrypted(value):
            return value
        # Convert to string for encryption
        encrypted_data = self._fernet.encrypt(str(value).encode('utf-8'))
        return base64.b64encode(encrypted_data).decode('utf-8')

    def from_db_value(self, value, expression, connection):
        if value is None or not isinstance(value, str):
            return value
        if not self._is_valid_base64(value):
            return value
        try:
            decrypted_data = self._fernet.decrypt(base64.b64decode(value.encode('utf-8')))
            result = decrypted_data.decode('utf-8')
            if isinstance(self, (EncryptedIntegerField, EncryptedPositiveIntegerField)):
                return int(result)
            return result
        except Exception:
            return value

    def to_python(self, value):
        if value is None:
            return None
        if isinstance(self, (EncryptedIntegerField, EncryptedPositiveIntegerField)):
            try:
                return int(value)
            except (ValueError, TypeError):
                return 0
        return str(value)

class EncryptedCharField(EncryptedFieldMixin, models.CharField):
    def get_db_prep_value(self, value, connection, prepared=False):
        return self.get_prep_value(self.to_python(value))

class EncryptedTextField(EncryptedFieldMixin, models.TextField):
    def get_db_prep_value(self, value, connection, prepared=False):
        return self.get_prep_value(self.to_python(value))

class EncryptedEmailField(EncryptedFieldMixin, models.EmailField):
    def get_db_prep_value(self, value, connection, prepared=False):
        return self.get_prep_value(self.to_python(value))

class EncryptedIntegerField(EncryptedFieldMixin, models.Field):
    """Encrypted IntegerField using Text backend to avoid max_length validation."""
    
    def db_type(self, connection):
        return 'text'  # Store encrypted data as text

    def clean(self, value, model_instance):
        if value is not None:
            try:
                value = int(value)
            except (ValueError, TypeError):
                raise ValidationError('Enter a valid integer.')
        return value

    def to_python(self, value):
        if value is None:
            return None
        if self._is_encrypted(value):
            try:
                decrypted_data = self._fernet.decrypt(base64.b64decode(value.encode('utf-8')))
                return int(decrypted_data.decode('utf-8'))
            except (ValueError, TypeError):
                raise ValidationError('Invalid encrypted integer value.')
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        if self._is_valid_base64(value):
            try:
                decrypted_data = self._fernet.decrypt(base64.b64decode(value.encode('utf-8')))
                return int(decrypted_data.decode('utf-8'))
            except (ValueError, TypeError):
                return 0
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        # Ensure value is an integer before encryption
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValidationError('Value must be an integer.')
        return self.get_prep_value(value)

class EncryptedPositiveIntegerField(EncryptedFieldMixin, models.Field):
    """Encrypted PositiveIntegerField using Text backend."""
    
    def db_type(self, connection):
        return 'text'  # Store encrypted data as text

    def clean(self, value, model_instance):
        if value is not None:
            try:
                value = int(value)
                if value < 0:
                    raise ValidationError('Enter a valid positive integer.')
            except (ValueError, TypeError):
                raise ValidationError('Enter a valid positive integer.')
        return value

    def to_python(self, value):
        if value is None:
            return None
        if self._is_encrypted(value):
            try:
                decrypted_data = self._fernet.decrypt(base64.b64decode(value.encode('utf-8')))
                return int(decrypted_data.decode('utf-8'))
            except (ValueError, TypeError):
                raise ValidationError('Invalid encrypted positive integer value.')
        try:
            val = int(value)
            return max(0, val)
        except (ValueError, TypeError):
            return 0

    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        if self._is_valid_base64(value):
            try:
                decrypted_data = self._fernet.decrypt(base64.b64decode(value.encode('utf-8')))
                return int(decrypted_data.decode('utf-8'))
            except (ValueError, TypeError):
                return 0
        return value

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        try:
            value = int(value)
            if value < 0:
                raise ValidationError('Value must be a positive integer.')
        except (ValueError, TypeError):
            raise ValidationError('Value must be a positive integer.')
        return self.get_prep_value(value)

# Utility functions (unchanged)
def encrypt_value(value, key=None):
    if key is None:
        key = getattr(settings, 'FIELD_ENCRYPTION_KEY', None)
        if not key:
            raise ImproperlyConfigured('FIELD_ENCRYPTION_KEY must be set in settings')
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(str(value).encode('utf-8'))
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt_value(encrypted_value, key=None):
    if key is None:
        key = getattr(settings, 'FIELD_ENCRYPTION_KEY', None)
        if not key:
            raise ImproperlyConfigured('FIELD_ENCRYPTION_KEY must be set in settings')
    fernet = Fernet(key)
    try:
        decrypted_data = fernet.decrypt(base64.b64decode(encrypted_value.encode('utf-8')))
        return decrypted_data.decode('utf-8')
    except Exception as e:
        print(f"Decryption failed: {e}")
        return encrypted_value