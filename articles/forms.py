from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['nom', 'reference', 'categorie', 'prix', 'quantite_initiale', 'description', 'seuil_alerte']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de l\'article'
            }),
            'reference': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Référence unique'
            }),
            'categorie': forms.Select(attrs={
                'class': 'form-select'
            }),
            'prix': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'quantite_initiale': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Description de l\'article (optionnel)'
            }),
            'seuil_alerte': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '10'
            })
        }

    def clean_reference(self):
        reference = self.cleaned_data.get('reference')
        if reference:
            reference = reference.upper().strip()
            # Vérifier l'unicité seulement si c'est un nouvel article ou si la référence a changé
            if self.instance.pk:
                if Article.objects.exclude(pk=self.instance.pk).filter(reference=reference).exists():
                    raise forms.ValidationError("Cette référence existe déjà.")
            else:
                if Article.objects.filter(reference=reference).exists():
                    raise forms.ValidationError("Cette référence existe déjà.")
        return reference

    def clean_prix(self):
        prix = self.cleaned_data.get('prix')
        if prix is not None and prix <= 0:
            raise forms.ValidationError("Le prix doit être supérieur à 0.")
        return prix
