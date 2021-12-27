from django.db import models
from rest_framework_simplejwt.tokens import Token

from .system import User


class BlackListedToken(models.Model):
    token = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("token", "user")

    @classmethod
    def is_blacklisted(cls, user, token):
        # type: (User, Token) -> bool
        return cls.objects.filter(user=user, token=str(token)) == 0

    @classmethod
    def add(cls, user, token):
        # type: (User, str) -> None
        cls.objects.get_or_create(user=user, token=token)
