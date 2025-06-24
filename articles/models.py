from django.db import models
from django.db.models import Sum, Q

class Article(models.Model):
    CATEGORIES = [
        ('ELECTRONIQUE', 'Électronique'),
        ('VETEMENT', 'Vêtement'),
        ('ALIMENTAIRE', 'Alimentaire'),
        ('AUTRE', 'Autre'),
    ]

    nom = models.CharField(max_length=100, verbose_name="Nom")
    reference = models.CharField(max_length=100, unique=True, verbose_name="Référence")
    categorie = models.CharField(max_length=50, choices=CATEGORIES, default='AUTRE', verbose_name="Catégorie")
    prix = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire")
    quantite_initiale = models.PositiveIntegerField(default=0, verbose_name="Quantité initiale")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    date_ajout = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    seuil_alerte = models.PositiveIntegerField(default=10, verbose_name="Seuil d'alerte")

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['nom']

    def __str__(self):
        return f"{self.nom} ({self.reference})"

    def stock_disponible(self):
        """Calcule le stock disponible en temps réel"""
        from stocks.models import StockMovement

        entrees = StockMovement.objects.filter(
            article=self,
            mouvement_type='ENTREE'
        ).aggregate(total=Sum('quantite'))['total'] or 0

        sorties = StockMovement.objects.filter(
            article=self,
            mouvement_type='SORTIE'
        ).aggregate(total=Sum('quantite'))['total'] or 0

        stock = self.quantite_initiale + entrees - sorties
        return max(0, stock)  # Éviter les valeurs négatives

    def is_stock_critique(self):
        """Vérifie si le stock est en dessous du seuil d'alerte"""
        return self.stock_disponible() <= self.seuil_alerte

    def get_categorie_display_custom(self):
        """Retourne le nom de la catégorie pour l'affichage"""
        return dict(self.CATEGORIES).get(self.categorie, self.categorie)

    def stock_disponible(self):
        # Calculate stock dynamically based on movements
        total_entrees = self.mouvements.filter(mouvement_type='ENTREE').aggregate(total=Sum('quantite'))['total'] or 0
        total_sorties = self.mouvements.filter(mouvement_type='SORTIE').aggregate(total=Sum('quantite'))['total'] or 0
        return self.quantite_initiale + total_entrees - total_sorties
