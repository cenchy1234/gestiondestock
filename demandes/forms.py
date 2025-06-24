from django import forms
from django.core.exceptions import ValidationError
from .models import Demande
from articles.models import Article

class DemandeForm(forms.ModelForm):
    """Formulaire pour créer une demande"""
    
    class Meta:
        model = Demande
        fields = [
            'article', 
            'quantite_demandee', 
            'priorite', 
            'motif', 
            'date_livraison_souhaitee',
            'remarques'
        ]
        widgets = {
            'article': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_article',
                'onchange': 'checkStock()'
            }),
            'quantite_demandee': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'id': 'id_quantite',
                'onchange': 'checkStock()'
            }),
            'priorite': forms.Select(attrs={
                'class': 'form-select'
            }),
            'motif': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Expliquez pourquoi vous avez besoin de cet article...'
            }),
            'date_livraison_souhaitee': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'remarques': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Remarques supplémentaires (optionnel)...'
            }),
        }
        labels = {
            'article': 'Article demandé',
            'quantite_demandee': 'Quantité demandée',
            'priorite': 'Priorité',
            'motif': 'Motif de la demande',
            'date_livraison_souhaitee': 'Date de livraison souhaitée',
            'remarques': 'Remarques',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer les articles disponibles
        self.fields['article'].queryset = Article.objects.filter(
            quantite_initiale__gt=0
        ).order_by('nom')
        
        # Rendre certains champs obligatoires
        self.fields['motif'].required = True
        self.fields['date_livraison_souhaitee'].required = True
    
    def clean_quantite_demandee(self):
        quantite = self.cleaned_data.get('quantite_demandee')
        if quantite and quantite <= 0:
            raise ValidationError("La quantité doit être supérieure à 0.")
        return quantite
    
    def clean(self):
        cleaned_data = super().clean()
        article = cleaned_data.get('article')
        quantite_demandee = cleaned_data.get('quantite_demandee')
        
        if article and quantite_demandee:
            stock_disponible = article.stock_disponible()
            if quantite_demandee > stock_disponible:
                raise ValidationError(
                    f"Stock insuffisant. Disponible: {stock_disponible} unités."
                )
        
        return cleaned_data


class TraiterDemandeForm(forms.ModelForm):
    """Formulaire pour traiter une demande (approuver/rejeter)"""

    class Meta:
        model = Demande
        fields = ['quantite_accordee', 'commentaire_traitement']
        widgets = {
            'quantite_accordee': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'commentaire_traitement': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Commentaire sur le traitement de la demande...'
            }),
        }
        labels = {
            'quantite_accordee': 'Quantité accordée',
            'commentaire_traitement': 'Commentaire',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            if self.instance and self.instance.pk:
                # Pré-remplir la quantité accordée avec la quantité demandée
                self.fields['quantite_accordee'].initial = self.instance.quantite_demandee

                # Limiter la quantité accordée au stock disponible
                try:
                    stock_disponible = self.instance.article.stock_disponible()
                    self.fields['quantite_accordee'].widget.attrs['max'] = stock_disponible

                    # Ajouter des informations dans le help_text
                    self.fields['quantite_accordee'].help_text = (
                        f"Stock disponible: {stock_disponible} unités. "
                        f"Quantité demandée: {self.instance.quantite_demandee} unités."
                    )
                except:
                    # En cas d'erreur, utiliser des valeurs par défaut
                    self.fields['quantite_accordee'].help_text = "Vérifiez le stock disponible."
        except:
            pass  # Continuer même en cas d'erreur

    def clean_quantite_accordee(self):
        quantite_accordee = self.cleaned_data.get('quantite_accordee')

        if quantite_accordee:
            if quantite_accordee <= 0:
                raise ValidationError("La quantité accordée doit être supérieure à 0.")

            try:
                if self.instance:
                    stock_disponible = self.instance.article.stock_disponible()
                    if quantite_accordee > stock_disponible:
                        raise ValidationError(
                            f"Quantité accordée supérieure au stock disponible ({stock_disponible} unités)."
                        )
            except:
                pass  # Continuer même si la vérification échoue

        return quantite_accordee


class FiltreDemandeForm(forms.Form):
    """Formulaire pour filtrer les demandes"""
    
    STATUT_CHOICES = [('', 'Tous les statuts')] + Demande.STATUT_CHOICES
    PRIORITE_CHOICES = [('', 'Toutes les priorités')] + Demande.PRIORITE_CHOICES
    
    statut = forms.ChoiceField(
        choices=STATUT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )
    
    priorite = forms.ChoiceField(
        choices=PRIORITE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'})
    )
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Rechercher par numéro, article ou motif...'
        })
    )
    
    date_debut = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control form-control-sm',
            'type': 'date'
        })
    )
    
    date_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control form-control-sm',
            'type': 'date'
        })
    )
