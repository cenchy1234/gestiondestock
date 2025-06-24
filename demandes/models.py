from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from articles.models import Article

User = get_user_model()

class Demande(models.Model):
    """Modèle pour les demandes d'articles par les employés"""
    
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('APPROUVEE', 'Approuvée'),
        ('REJETEE', 'Rejetée'),
        ('TRAITEE', 'Traitée'),
    ]
    
    PRIORITE_CHOICES = [
        ('BASSE', 'Basse'),
        ('NORMALE', 'Normale'),
        ('HAUTE', 'Haute'),
        ('URGENTE', 'Urgente'),
    ]
    
    # Informations de base
    numero_demande = models.CharField(max_length=20, unique=True, editable=False)
    demandeur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='demandes')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='demandes')
    quantite_demandee = models.PositiveIntegerField()
    
    # Statut et priorité
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_ATTENTE')
    priorite = models.CharField(max_length=20, choices=PRIORITE_CHOICES, default='NORMALE')
    
    # Dates
    date_demande = models.DateTimeField(auto_now_add=True)
    date_traitement = models.DateTimeField(null=True, blank=True)
    date_livraison_souhaitee = models.DateField(null=True, blank=True)
    
    # Détails
    motif = models.TextField(help_text="Motif de la demande")
    remarques = models.TextField(blank=True, null=True)
    
    # Traitement
    traite_par = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='demandes_traitees'
    )
    commentaire_traitement = models.TextField(blank=True, null=True)
    quantite_accordee = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-date_demande']
        verbose_name = 'Demande'
        verbose_name_plural = 'Demandes'
    
    def __str__(self):
        return f"Demande {self.numero_demande} - {self.article.nom} ({self.quantite_demandee})"
    
    def save(self, *args, **kwargs):
        if not self.numero_demande:
            # Générer un numéro de demande unique
            from datetime import datetime
            today = datetime.now()
            prefix = f"DEM{today.strftime('%Y%m%d')}"
            
            # Trouver le dernier numéro du jour
            last_demande = Demande.objects.filter(
                numero_demande__startswith=prefix
            ).order_by('-numero_demande').first()
            
            if last_demande:
                last_number = int(last_demande.numero_demande[-3:])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.numero_demande = f"{prefix}{new_number:03d}"
        
        super().save(*args, **kwargs)
    
    @property
    def peut_etre_approuvee(self):
        """Vérifie si la demande peut être approuvée (stock suffisant)"""
        return self.article.stock_disponible() >= self.quantite_demandee
    
    @property
    def stock_disponible(self):
        """Retourne le stock disponible de l'article demandé"""
        return self.article.stock_disponible()
    
    @property
    def est_urgente(self):
        """Vérifie si la demande est urgente"""
        return self.priorite == 'URGENTE'
    
    @property
    def est_en_retard(self):
        """Vérifie si la demande est en retard par rapport à la date souhaitée"""
        if self.date_livraison_souhaitee and self.statut == 'EN_ATTENTE':
            from datetime import date
            return date.today() > self.date_livraison_souhaitee
        return False
    
    def approuver(self, user, quantite_accordee=None, commentaire=""):
        """Approuve la demande"""
        from django.utils import timezone
        self.statut = 'APPROUVEE'
        self.traite_par = user
        self.quantite_accordee = quantite_accordee or self.quantite_demandee
        self.commentaire_traitement = commentaire
        self.date_traitement = timezone.now()
        self.save()

    def rejeter(self, user, commentaire=""):
        """Rejette la demande"""
        from django.utils import timezone
        self.statut = 'REJETEE'
        self.traite_par = user
        self.commentaire_traitement = commentaire
        self.date_traitement = timezone.now()
        self.save()
    
    def traiter(self, user, commentaire=""):
        """Marque la demande comme traitée (livrée)"""
        if self.statut == 'APPROUVEE':
            from django.utils import timezone
            self.statut = 'TRAITEE'
            self.traite_par = user
            if commentaire:
                self.commentaire_traitement = commentaire
            self.date_traitement = timezone.now()
            self.save()

            # Créer un mouvement de stock de sortie
            try:
                from stocks.models import StockMovement
                StockMovement.objects.create(
                    article=self.article,
                    mouvement_type='SORTIE',
                    quantite=self.quantite_accordee or self.quantite_demandee,
                    remarque=f"Demande {self.numero_demande} - {self.motif}"
                )
            except Exception as e:
                # En cas d'erreur, continuer mais noter l'erreur
                print(f"Erreur lors de la création du mouvement de stock: {e}")
                pass


class HistoriqueDemande(models.Model):
    """Historique des modifications des demandes"""
    
    demande = models.ForeignKey(Demande, on_delete=models.CASCADE, related_name='historique')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    details = models.TextField(blank=True)
    date_action = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_action']
        verbose_name = 'Historique de demande'
        verbose_name_plural = 'Historiques de demandes'
    
    def __str__(self):
        return f"{self.demande.numero_demande} - {self.action} par {self.utilisateur.username}"
