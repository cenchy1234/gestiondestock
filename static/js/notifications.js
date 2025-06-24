/**
 * Système de notifications push en temps réel
 * Fonctionnalité AMAZING pour impressionner ! 🚀
 */

class NotificationSystem {
    constructor() {
        this.notifications = [];
        this.init();
    }

    init() {
        this.createNotificationContainer();
        this.requestPermission();
        this.startPeriodicCheck();
    }

    createNotificationContainer() {
        if (!document.getElementById('notification-container')) {
            const container = document.createElement('div');
            container.id = 'notification-container';
            container.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                max-width: 400px;
            `;
            document.body.appendChild(container);
        }
    }

    async requestPermission() {
        if ('Notification' in window && Notification.permission === 'default') {
            await Notification.requestPermission();
        }
    }

    showNotification(title, message, type = 'info', duration = 5000) {
        // Notification dans le navigateur
        if ('Notification' in window && Notification.permission === 'granted') {
            const notification = new Notification(title, {
                body: message,
                icon: '/static/img/logo.png',
                badge: '/static/img/badge.png'
            });

            setTimeout(() => notification.close(), duration);
        }

        // Notification visuelle dans l'interface
        this.showToast(title, message, type, duration);
    }

    showToast(title, message, type, duration) {
        const toast = document.createElement('div');
        const toastId = 'toast-' + Date.now();
        
        const bgClass = {
            'success': 'bg-success',
            'error': 'bg-danger',
            'warning': 'bg-warning',
            'info': 'bg-info'
        }[type] || 'bg-info';

        const icon = {
            'success': 'fa-check-circle',
            'error': 'fa-exclamation-triangle',
            'warning': 'fa-exclamation-circle',
            'info': 'fa-info-circle'
        }[type] || 'fa-info-circle';

        toast.id = toastId;
        toast.className = `toast show ${bgClass} text-white mb-2`;
        toast.style.cssText = `
            animation: slideInRight 0.5s ease-out;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;

        toast.innerHTML = `
            <div class="toast-header ${bgClass} text-white border-0">
                <i class="fas ${icon} me-2"></i>
                <strong class="me-auto">${title}</strong>
                <button type="button" class="btn-close btn-close-white" onclick="this.parentElement.parentElement.remove()"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        `;

        document.getElementById('notification-container').appendChild(toast);

        // Auto-remove après la durée spécifiée
        setTimeout(() => {
            const element = document.getElementById(toastId);
            if (element) {
                element.style.animation = 'slideOutRight 0.5s ease-out';
                setTimeout(() => element.remove(), 500);
            }
        }, duration);
    }

    async checkForAlerts() {
        try {
            const response = await fetch('/api/alerts/');
            const result = await response.json();
            
            if (result.success && result.data.length > 0) {
                const newAlerts = result.data.filter(alert => 
                    !this.notifications.some(notif => 
                        notif.title === alert.title && notif.message === alert.message
                    )
                );

                newAlerts.forEach(alert => {
                    this.showNotification(
                        alert.title,
                        alert.message,
                        alert.level === 'danger' ? 'error' : alert.level,
                        8000
                    );
                    
                    this.notifications.push({
                        title: alert.title,
                        message: alert.message,
                        timestamp: new Date()
                    });
                });
            }
        } catch (error) {
            console.error('Erreur lors de la vérification des alertes:', error);
        }
    }

    startPeriodicCheck() {
        // Vérifier les alertes toutes les 2 minutes
        setInterval(() => {
            this.checkForAlerts();
        }, 120000);

        // Première vérification après 5 secondes
        setTimeout(() => {
            this.checkForAlerts();
        }, 5000);
    }

    // Méthode pour déclencher une notification manuelle
    triggerStockAlert(articleName, currentStock, threshold) {
        this.showNotification(
            '🚨 Alerte Stock Critique',
            `L'article "${articleName}" a un stock de ${currentStock} unités (seuil: ${threshold})`,
            'warning',
            10000
        );
    }

    // Méthode pour les notifications de succès
    showSuccess(message) {
        this.showNotification('✅ Succès', message, 'success', 3000);
    }

    // Méthode pour les notifications d'erreur
    showError(message) {
        this.showNotification('❌ Erreur', message, 'error', 5000);
    }
}

// Styles CSS pour les animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }

    .toast {
        border-radius: 8px !important;
        border: none !important;
    }

    .toast-header {
        border-radius: 8px 8px 0 0 !important;
    }
`;
document.head.appendChild(style);

// Système d'animations globales
class AnimationSystem {
    constructor() {
        this.init();
    }

    init() {
        this.observeElements();
        this.addHoverEffects();
        this.initCounterAnimations();
    }

    observeElements() {
        // Observer pour les animations au scroll
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fadeInUp');
                }
            });
        }, { threshold: 0.1 });

        // Observer tous les éléments avec la classe animate-on-scroll
        document.querySelectorAll('.animate-on-scroll').forEach(el => {
            observer.observe(el);
        });
    }

    addHoverEffects() {
        // Effet de survol pour les cartes
        document.querySelectorAll('.card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-5px)';
                card.style.boxShadow = '0 8px 30px rgba(0,0,0,0.2)';
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0)';
                card.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
            });
        });

        // Effet de survol pour les boutons
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('mouseenter', () => {
                btn.style.transform = 'translateY(-2px)';
            });

            btn.addEventListener('mouseleave', () => {
                btn.style.transform = 'translateY(0)';
            });
        });
    }

    initCounterAnimations() {
        // Animation des compteurs
        const counters = document.querySelectorAll('[data-counter]');
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-counter'));
            this.animateCounter(counter, target);
        });
    }

    animateCounter(element, target) {
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;

        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current);
        }, 16);
    }
}

// Initialiser le système de notifications
let notificationSystem;
let animationSystem;

document.addEventListener('DOMContentLoaded', function() {
    notificationSystem = new NotificationSystem();
    animationSystem = new AnimationSystem();

    // Vérifier si c'est la première visite de la session
    const hasShownWelcome = sessionStorage.getItem('welcomeShown');

    if (!hasShownWelcome) {
        // Notification de bienvenue une seule fois par session
        setTimeout(() => {
            notificationSystem.showNotification(
                '🌿 Bienvenue',
                'Système de gestion de stock chargé avec succès !',
                'success',
                3000
            );
            sessionStorage.setItem('welcomeShown', 'true');
        }, 1000);
    }

    // Ajouter la classe animate-on-scroll aux éléments
    document.querySelectorAll('.card, .btn, .table').forEach(el => {
        el.classList.add('animate-on-scroll');
    });
});

// Exposer globalement pour utilisation dans d'autres scripts
window.notificationSystem = notificationSystem;
window.animationSystem = animationSystem;
