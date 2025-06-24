from django.db import models
from articles.models import Article

class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField(blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nom

class Commande(models.Model):
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('EN_COURS', 'En cours'),
        ('LIVREE', 'Livrée'),
        ('ANNULEE', 'Annulée')
    ]
    
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, related_name='commandes')
    article = models.ForeignKey('articles.Article', on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    date_commande = models.DateTimeField(auto_now_add=True)
    date_livraison = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Commande #{self.id} - {self.fournisseur.nom}"
