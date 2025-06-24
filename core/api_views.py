"""
API Views pour les fonctionnalités temps réel et IA
"""

import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .ai_analytics import StockAI, RealtimeNotifications

@login_required
def live_stats_api(request):
    """API pour les statistiques en temps réel"""
    try:
        stats = RealtimeNotifications.get_live_stats()
        return JsonResponse({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
def ai_predictions_api(request):
    """API pour les prédictions IA"""
    try:
        days_ahead = int(request.GET.get('days', 30))
        predictions = StockAI.predict_stock_rupture(days_ahead)
        
        # Sérialiser les données
        serialized_predictions = []
        for pred in predictions:
            serialized_predictions.append({
                'article_id': pred['article'].id,
                'article_nom': pred['article'].nom,
                'article_reference': pred['article'].reference,
                'days_until_rupture': pred['days_until_rupture'],
                'risk_level': pred['risk_level'],
                'avg_consumption': pred['avg_consumption'],
                'current_stock': pred['current_stock'],
                'recommended_order': pred['recommended_order']
            })
        
        return JsonResponse({
            'success': True,
            'data': serialized_predictions
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
def smart_recommendations_api(request):
    """API pour les recommandations intelligentes"""
    try:
        recommendations = StockAI.get_smart_recommendations()
        return JsonResponse({
            'success': True,
            'data': recommendations
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
def performance_metrics_api(request):
    """API pour les métriques de performance"""
    try:
        metrics = StockAI.get_performance_metrics()
        return JsonResponse({
            'success': True,
            'data': metrics
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
def alerts_api(request):
    """API pour les alertes intelligentes"""
    try:
        alerts = StockAI.generate_alerts()
        
        # Sérialiser les alertes
        serialized_alerts = []
        for alert in alerts:
            serialized_alerts.append({
                'type': alert['type'],
                'level': alert['level'],
                'title': alert['title'],
                'message': alert['message'],
                'action_url': alert['action_url'],
                'timestamp': alert['timestamp'].isoformat()
            })
        
        return JsonResponse({
            'success': True,
            'data': serialized_alerts
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class NotificationWebhook(View):
    """Webhook pour les notifications push"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            notification_type = data.get('type')
            
            if notification_type == 'stock_alert':
                # Traiter l'alerte de stock
                article_id = data.get('article_id')
                # Logique de traitement...
                
            return JsonResponse({
                'success': True,
                'message': 'Notification processed'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
