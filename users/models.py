from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ADMIN = 'ADMIN'
    GESTIONNAIRE = 'GESTIONNAIRE'
    EMPLOYE = 'EMPLOYE'

    ROLE_CHOICES = [
        (ADMIN, 'Administrateur'),
        (GESTIONNAIRE, 'Gestionnaire de stock'),
        (EMPLOYE, 'Employé'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=EMPLOYE)

    def __str__(self):
        return f"{self.username} ({self.role})"
