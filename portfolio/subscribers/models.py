from django.db import models
from django.contrib.auth.models import AbstractUser

class Subscribers(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)

    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'

    def __str__(self):
        return self.username