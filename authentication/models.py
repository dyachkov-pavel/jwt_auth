from django.db import models
from django.contrib.auth.models import AbstractUser
import bcrypt


class User(AbstractUser):
    refresh_token = models.BinaryField(null=True, blank=True)
    refresh_token_count = models.IntegerField(default=0)

    def set_refresh_token(self, refresh_token):
        refresh_token_bytes = refresh_token.encode()
        self.refresh_token = bcrypt.hashpw(refresh_token_bytes, bcrypt.gensalt())

    def check_refresh_token(self, refresh_token):
        refresh_token_bytes = refresh_token.encode()
        given_refresh_token = bcrypt.hashpw(refresh_token_bytes, bcrypt.gensalt())
        return bcrypt.checkpw(given_refresh_token, self.refresh_token)
