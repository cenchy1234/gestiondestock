from datetime import datetime
from .models import ActionLog
from fournisseurs.models import Commande

def log_action(user, action_description):
    """
    Log user actions in the system
    """
    ActionLog.objects.create(
        user=user,
        action=action_description
    )

def get_fournisseur_commandes(fournisseur_id=None):
    """Get all commands for a specific supplier or all suppliers if no ID provided"""
    if fournisseur_id:
        return Commande.objects.filter(fournisseur_id=fournisseur_id)
    return Commande.objects.all()

def create_fournisseur_commande(fournisseur_id, article_data, date=None):
    """Create a new supplier command"""
    return Commande.objects.create(
        fournisseur_id=fournisseur_id,
        article=article_data['article'],
        quantite=article_data['quantite'],
        date_commande=date or datetime.now()
    )
