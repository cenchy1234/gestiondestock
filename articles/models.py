from django.db import models

class Article(models.Model):
    CATEGORIES = [
        ('ELECTRONIQUE', 'Électronique'),
        ('VETEMENT', 'Vêtement'),
        ('ALIMENTAIRE', 'Alimentaire'),
        ('AUTRE', 'Autre'),
    ]

    nom = models.CharField(max_length=100)
    reference = models.CharField(max_length=100, unique=True)
    categorie = models.CharField(max_length=50, choices=CATEGORIES, default='AUTRE')
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    quantite_initiale = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} ({self.reference})"
