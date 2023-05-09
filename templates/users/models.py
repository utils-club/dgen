"""implements this:
https://www.django-rest-framework.org/api-guide/authentication/
"""
from django.db import models
from django.contrib.auth.models import User


class PlatformUser(User):
    description = models.TextField(blank=True)
