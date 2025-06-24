from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = [
        ('ADMIN', 'Administrateur'),
        ('STOCK_MANAGER', 'Gestionnaire de Stock'),
        ('EMPLOYEE', 'Employé')
    ]
    role = models.CharField(
        max_length=15, 
        choices=ROLES,
        default='EMPLOYEE',
        verbose_name='Rôle'
    )

    def is_admin(self):
        return self.role == 'ADMIN'

    def is_stock_manager(self):
        return self.role == 'STOCK_MANAGER'
    
    def can_manage_users(self):
        # Administrateur uniquement
        return self.role == 'ADMIN'

    def can_configure_system(self):
        # Administrateur uniquement
        return self.role == 'ADMIN'

    @property
    def can_manage_stock(self):
        # Administrateur ou gestionnaire de stock
        return self.role in ['ADMIN', 'STOCK_MANAGER']

    def can_view_stock(self):
        # Tous les rôles peuvent consulter le stock
        return self.role in ['ADMIN', 'STOCK_MANAGER', 'EMPLOYEE']

    def can_request_stock(self):
        # Employé uniquement (ou plus si besoin)
        return self.role == 'EMPLOYEE'
