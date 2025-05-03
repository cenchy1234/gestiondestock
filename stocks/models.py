from django.db import models
from articles.models import Article

class StockMovement(models.Model):
    TYPES = [
        ('ENTREE', 'Entrée'),
        ('SORTIE', 'Sortie'),
    ]

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    mouvement_type = models.CharField(max_length=10, choices=TYPES)
    quantite = models.PositiveIntegerField()
    date_mouvement = models.DateTimeField(auto_now_add=True)
    remarque = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.mouvement_type} - {self.article.nom} ({self.quantite})"
