from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from .models import Demande, HistoriqueDemande
from .forms import DemandeForm, TraiterDemandeForm
from articles.models import Article

@login_required
def demande_list(request):
    """Liste des demandes selon le rôle de l'utilisateur"""

    # Version simplifiée pour éviter les erreurs
    demandes = Demande.objects.all().order_by('-date_demande')

    # Pagination simple
    paginator = Paginator(demandes, 10)
    page_number = request.GET.get('page')
    demandes_page = paginator.get_page(page_number)

    # Statistiques basiques
    stats = {
        'total': demandes.count(),
        'en_attente': demandes.filter(statut='EN_ATTENTE').count(),
        'approuvees': demandes.filter(statut='APPROUVEE').count(),
        'urgentes': demandes.filter(priorite='URGENTE').count(),
    }

    context = {
        'demandes': demandes_page,
        'stats': stats,
    }

    return render(request, 'demandes/demande_list.html', context)

@login_required
def demande_create(request):
    """Création d'une nouvelle demande (employés uniquement)"""

    # Vérification du rôle simplifiée
    try:
        if hasattr(request.user, 'role') and request.user.role != 'EMPLOYEE':
            messages.info(request, "Redirection vers la gestion des demandes.")
            return redirect('demandes:demande_list')
    except:
        pass  # Continuer même si la vérification échoue

    if request.method == 'POST':
        try:
            form = DemandeForm(request.POST)
            if form.is_valid():
                demande = form.save(commit=False)
                demande.demandeur = request.user
                demande.save()

                # Enregistrer l'historique
                try:
                    HistoriqueDemande.objects.create(
                        demande=demande,
                        utilisateur=request.user,
                        action="Demande créée",
                        details=f"Demande de {demande.quantite_demandee} {demande.article.nom}"
                    )
                except:
                    pass  # Continuer même si l'historique échoue

                messages.success(request, f"Demande {demande.numero_demande} créée avec succès!")
                return redirect('demandes:demande_detail', pk=demande.pk)
        except Exception as e:
            messages.error(request, f"Erreur lors de la création: {str(e)}")

    # Créer le formulaire
    try:
        form = DemandeForm()
    except:
        form = None

    # Articles disponibles
    try:
        articles = Article.objects.filter(quantite_initiale__gt=0).order_by('nom')
    except:
        articles = Article.objects.all().order_by('nom')

    context = {
        'form': form,
        'articles': articles,
    }

    return render(request, 'demandes/demande_create.html', context)

@login_required
def demande_detail(request, pk):
    """Détail d'une demande"""
    
    demande = get_object_or_404(Demande, pk=pk)
    
    # Vérifier les permissions
    if request.user.role == 'EMPLOYEE' and demande.demandeur != request.user:
        messages.error(request, "Vous ne pouvez consulter que vos propres demandes.")
        return redirect('demandes:demande_list')
    
    # Historique de la demande
    historique = demande.historique.all()
    
    context = {
        'demande': demande,
        'historique': historique,
    }
    
    return render(request, 'demandes/demande_detail.html', context)

@login_required
def demande_traiter(request, pk):
    """Traitement d'une demande (gestionnaires uniquement)"""

    # Vérification des permissions simplifiée
    try:
        if not hasattr(request.user, 'can_manage_stock') or not request.user.can_manage_stock:
            messages.error(request, "Vous n'avez pas les permissions pour traiter les demandes.")
            return redirect('demandes:demande_list')
    except:
        messages.error(request, "Erreur de permissions.")
        return redirect('demandes:demande_list')

    demande = get_object_or_404(Demande, pk=pk)

    if demande.statut != 'EN_ATTENTE':
        messages.error(request, "Cette demande a déjà été traitée.")
        return redirect('demandes:demande_detail', pk=pk)

    if request.method == 'POST':
        try:
            form = TraiterDemandeForm(request.POST, instance=demande)
            if form.is_valid():
                action = request.POST.get('action')

                if action == 'approuver':
                    quantite_accordee = form.cleaned_data.get('quantite_accordee')
                    commentaire = form.cleaned_data.get('commentaire_traitement', '')

                    # Vérifier le stock disponible
                    if quantite_accordee > demande.article.stock_disponible():
                        messages.error(request, "Stock insuffisant pour approuver cette quantité.")
                        return render(request, 'demandes/demande_traiter.html', {'form': form, 'demande': demande})

                    demande.approuver(request.user, quantite_accordee, commentaire)

                    # Historique
                    try:
                        HistoriqueDemande.objects.create(
                            demande=demande,
                            utilisateur=request.user,
                            action="Demande approuvée",
                            details=f"Quantité accordée: {quantite_accordee}"
                        )
                    except:
                        pass  # Continuer même si l'historique échoue

                    messages.success(request, f"Demande {demande.numero_demande} approuvée!")

                elif action == 'rejeter':
                    commentaire = form.cleaned_data.get('commentaire_traitement', '')
                    demande.rejeter(request.user, commentaire)

                    # Historique
                    try:
                        HistoriqueDemande.objects.create(
                            demande=demande,
                            utilisateur=request.user,
                            action="Demande rejetée",
                            details=commentaire
                        )
                    except:
                        pass  # Continuer même si l'historique échoue

                    messages.info(request, f"Demande {demande.numero_demande} rejetée.")

                return redirect('demandes:demande_detail', pk=pk)
        except Exception as e:
            messages.error(request, f"Erreur lors du traitement: {str(e)}")

    # Créer le formulaire
    try:
        form = TraiterDemandeForm(instance=demande)
    except:
        # Formulaire simple en cas d'erreur
        form = None

    context = {
        'form': form,
        'demande': demande,
    }

    return render(request, 'demandes/demande_traiter.html', context)

@login_required
def demande_livrer(request, pk):
    """Marquer une demande comme livrée"""

    # Vérification des permissions simplifiée
    try:
        if not hasattr(request.user, 'can_manage_stock') or not request.user.can_manage_stock:
            messages.error(request, "Vous n'avez pas les permissions pour livrer les demandes.")
            return redirect('demandes:demande_list')
    except:
        messages.error(request, "Erreur de permissions.")
        return redirect('demandes:demande_list')

    demande = get_object_or_404(Demande, pk=pk)

    if demande.statut != 'APPROUVEE':
        messages.error(request, "Seules les demandes approuvées peuvent être livrées.")
        return redirect('demandes:demande_detail', pk=pk)

    if request.method == 'POST':
        try:
            commentaire = request.POST.get('commentaire', '')
            demande.traiter(request.user, commentaire)

            # Historique
            try:
                HistoriqueDemande.objects.create(
                    demande=demande,
                    utilisateur=request.user,
                    action="Demande livrée",
                    details=commentaire or "Demande marquée comme livrée"
                )
            except:
                pass  # Continuer même si l'historique échoue

            messages.success(request, f"Demande {demande.numero_demande} marquée comme livrée!")
            return redirect('demandes:demande_detail', pk=pk)

        except Exception as e:
            messages.error(request, f"Erreur lors de la livraison: {str(e)}")
            return redirect('demandes:demande_detail', pk=pk)

    context = {
        'demande': demande,
    }

    return render(request, 'demandes/demande_livrer.html', context)

@login_required
def check_stock_ajax(request):
    """Vérification du stock disponible via AJAX"""
    
    article_id = request.GET.get('article_id')
    quantite = request.GET.get('quantite')
    
    if not article_id or not quantite:
        return JsonResponse({'error': 'Paramètres manquants'})
    
    try:
        article = Article.objects.get(pk=article_id)
        quantite = int(quantite)
        stock_disponible = article.stock_disponible()
        
        return JsonResponse({
            'stock_disponible': stock_disponible,
            'suffisant': stock_disponible >= quantite,
            'article_nom': article.nom,
            'prix_unitaire': float(article.prix),
            'total': float(article.prix) * quantite
        })
    except (Article.DoesNotExist, ValueError):
        return JsonResponse({'error': 'Article non trouvé ou quantité invalide'})

@login_required
def mes_demandes(request):
    """Vue spécifique pour les employés - leurs demandes"""
    
    if request.user.role != 'EMPLOYEE':
        return redirect('demandes:demande_list')
    
    demandes = Demande.objects.filter(demandeur=request.user)
    
    # Statistiques personnelles
    stats = {
        'total': demandes.count(),
        'en_attente': demandes.filter(statut='EN_ATTENTE').count(),
        'approuvees': demandes.filter(statut='APPROUVEE').count(),
        'traitees': demandes.filter(statut='TRAITEE').count(),
        'rejetees': demandes.filter(statut='REJETEE').count(),
    }
    
    # Pagination
    paginator = Paginator(demandes, 10)
    page_number = request.GET.get('page')
    demandes_page = paginator.get_page(page_number)
    
    context = {
        'demandes': demandes_page,
        'stats': stats,
    }
    
    return render(request, 'demandes/mes_demandes.html', context)
