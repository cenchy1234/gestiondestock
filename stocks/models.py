from django.db import models
from django.utils import timezone
from articles.models import Article

class StockMovement(models.Model):
    TYPES = [
        ('ENTREE', 'Entrée'),
        ('SORTIE', 'Sortie'),
    ]

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='mouvements', verbose_name="Article")
    mouvement_type = models.CharField(max_length=10, choices=TYPES, verbose_name="Type de mouvement")
    quantite = models.PositiveIntegerField(verbose_name="Quantité")
    date_mouvement = models.DateTimeField(default=timezone.now, verbose_name="Date du mouvement")
    remarque = models.TextField(blank=True, null=True, verbose_name="Remarque")

    class Meta:
        verbose_name = "Mouvement de stock"
        verbose_name_plural = "Mouvements de stock"
        ordering = ['-date_mouvement']

    def __str__(self):
        return f"{self.get_mouvement_type_display()} - {self.article.nom} ({self.quantite} unités) - {self.date_mouvement.strftime('%d/%m/%Y %H:%M')}"

    def clean(self):
        """Validation personnalisée"""
        from django.core.exceptions import ValidationError
        if self.mouvement_type == 'SORTIE' and self.article:
            stock_disponible = self.article.stock_disponible()
            if self.quantite > stock_disponible:
                raise ValidationError(
                    f"Stock insuffisant pour l'article '{self.article.nom}'. "
                    f"Stock disponible : {stock_disponible}, quantité demandée : {self.quantite}"
                )
