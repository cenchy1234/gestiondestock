from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Article
from .forms import ArticleForm
from core.decorators import can_view_stock_required, stock_manager_required

@can_view_stock_required
def article_list(request):
    query = request.GET.get('q', '')
    if query:
        articles = Article.objects.filter(nom__icontains=query) | Article.objects.filter(reference__icontains=query)
    else:
        articles = Article.objects.all()

    if not articles.exists():
        articles = None
    return render(request, 'articles/article_list.html', {'articles': articles, 'query': query})

@stock_manager_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            messages.success(request, f'Article "{article.nom}" créé avec succès!')
            return redirect('articles:article_list')
    else:
        form = ArticleForm()
    return render(request, 'articles/article_form.html', {'form': form, 'title': 'Ajouter un article'})

@stock_manager_required
def article_update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, f'Article "{article.nom}" modifié avec succès!')
            return redirect('articles:article_list')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/article_form.html', {'form': form, 'title': 'Modifier l\'article', 'article': article})

@stock_manager_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article_name = article.nom
        article.delete()
        messages.success(request, f'Article "{article_name}" supprimé avec succès!')
        return redirect('articles:article_list')
    return render(request, 'articles/article_confirm_delete.html', {'article': article})
    
    @login_required
    def dashboard(request):
        total_articles = Article.objects.count()
        recent_articles = Article.objects.order_by('-created_at')[:5]  # Assuming 'created_at' is a field in Article
        return render(request, 'articles/dashboard.html', {
            'total_articles': total_articles,
            'recent_articles': recent_articles
        })