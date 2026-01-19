from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_buyer = models.BooleanField(default=False)
    is_supplier = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    @property
    def role(self):
        if self.is_superuser:
            return 'admin'
        if self.is_supplier:
            return 'supplier'
        if self.is_buyer:
            return 'buyer'
        return None
