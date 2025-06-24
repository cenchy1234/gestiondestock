from django import forms
from django.utils import timezone
from .models import StockMovement

class StockMovementForm(forms.ModelForm):
    date_mouvement = forms.DateTimeField(
        initial=timezone.now,
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local'
        }),
        help_text="Date et heure du mouvement de stock"
    )

    class Meta:
        model = StockMovement
        fields = ['article', 'mouvement_type', 'quantite', 'date_mouvement', 'remarque']
        widgets = {
            'article': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'mouvement_type': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'quantite': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'required': True
            }),
            'remarque': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Remarque optionnelle sur ce mouvement de stock'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Formater la date initiale pour le widget datetime-local
        if not self.instance.pk:
            now = timezone.now()
            self.fields['date_mouvement'].initial = now.strftime('%Y-%m-%dT%H:%M')

    def clean(self):
        cleaned_data = super().clean()
        article = cleaned_data.get('article')
        mouvement_type = cleaned_data.get('mouvement_type')
        quantite = cleaned_data.get('quantite')

        if article and mouvement_type and quantite:
            # Check if the stock is sufficient for "SORTIE"
            if mouvement_type == 'SORTIE':
                stock_disponible = article.stock_disponible()
                if stock_disponible == 0:
                    raise forms.ValidationError(
                        f"❌ ERREUR : Aucun stock disponible pour l'article '{article.nom}' ! "
                        f"Impossible d'effectuer une sortie."
                    )
                elif quantite > stock_disponible:
                    raise forms.ValidationError(
                        f"❌ ERREUR : Stock insuffisant pour l'article '{article.nom}' !\n\n"
                        f"📦 Stock actuellement disponible : {stock_disponible} unités\n"
                        f"📤 Quantité demandée en sortie : {quantite} unités\n"
                        f"⚠️ Il manque {quantite - stock_disponible} unités pour effectuer cette sortie.\n\n"
                        f"💡 Solutions possibles :\n"
                        f"   • Réduire la quantité à {stock_disponible} unités maximum\n"
                        f"   • Effectuer d'abord une entrée de stock pour augmenter le stock disponible"
                    )
        return cleaned_data

    def clean_quantite(self):
        quantite = self.cleaned_data.get('quantite')
        if quantite is not None and quantite <= 0:
            raise forms.ValidationError("La quantité doit être supérieure à 0.")
        return quantite
