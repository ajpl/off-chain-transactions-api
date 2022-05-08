from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
from django.db.models import BinaryField


class EncryptedField(BinaryField):
    """Custom Encrypted Field"""

    f = Fernet(settings.BALANCE_KEY)

    def from_db_value(self, value, expression, connection):
        try:
            return self.f.decrypt(value)
        except (TypeError, InvalidToken):
            return b""

    def get_prep_value(self, value):
        return self.f.encrypt(value)
