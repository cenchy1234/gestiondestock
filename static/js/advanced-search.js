/**
 * Système de Recherche Avancée avec Scanner de Codes-Barres Simulé
 * Fonctionnalité innovante pour la gestion de stock
 */

class AdvancedSearch {
    constructor() {
        this.currentTab = 'text';
        this.isScanning = false;
        this.searchResults = [];
        this.filters = {
            category: '',
            stock_status: '',
            price_range: ''
        };
        this.init();
    }

    init() {
        this.createSearchInterface();
        this.bindEvents();
        this.initBarcodeScanner();
    }

    createSearchInterface() {
        const searchContainer = document.getElementById('advanced-search-container');
        if (!searchContainer) return;

        searchContainer.innerHTML = `
            <div class="advanced-search fade-in">
                <div class="search-tabs">
                    <button class="search-tab active" data-tab="text">
                        <i class="fas fa-search me-2"></i>Recherche Textuelle
                    </button>
                    <button class="search-tab" data-tab="barcode">
                        <i class="fas fa-barcode me-2"></i>Scanner Code-Barres
                    </button>
                    <button class="search-tab" data-tab="filters">
                        <i class="fas fa-filter me-2"></i>Filtres Avancés
                    </button>
                </div>

                <div class="search-content">
                    <!-- Recherche Textuelle -->
                    <div class="search-panel" id="text-panel">
                        <div class="search-input-group">
                            <input type="text" class="search-input" id="text-search" 
                                   placeholder="Rechercher par nom, référence, description...">
                            <button class="search-btn" onclick="advancedSearch.performTextSearch()">
                                <i class="fas fa-search"></i>
                            </button>
                        </div>
                        <div class="quick-filters">
                            <span class="filter-chip" onclick="advancedSearch.quickFilter('stock_critique')">
                                Stock Critique
                            </span>
                            <span class="filter-chip" onclick="advancedSearch.quickFilter('nouveaux')">
                                Nouveaux Articles
                            </span>
                            <span class="filter-chip" onclick="advancedSearch.quickFilter('populaires')">
                                Plus Populaires
                            </span>
                        </div>
                    </div>

                    <!-- Scanner Code-Barres -->
                    <div class="search-panel" id="barcode-panel" style="display: none;">
                        <div class="barcode-scanner">
                            <h4><i class="fas fa-barcode me-2"></i>Scanner de Code-Barres</h4>
                            <div class="scanner-animation" id="scanner-area">
                                <div class="scanner-line" id="scanner-line"></div>
                                <div class="scanner-text" id="scanner-text">
                                    Cliquez pour simuler un scan
                                </div>
                            </div>
                            <button class="btn btn-success" onclick="advancedSearch.toggleScanner()">
                                <i class="fas fa-play me-2"></i>
                                <span id="scanner-btn-text">Démarrer le Scanner</span>
                            </button>
                            <div class="mt-3">
                                <small class="text-muted">
                                    <i class="fas fa-info-circle me-1"></i>
                                    Mode simulation - Cliquez sur la zone de scan pour tester
                                </small>
                            </div>
                        </div>
                    </div>

                    <!-- Filtres Avancés -->
                    <div class="search-panel" id="filters-panel" style="display: none;">
                        <div class="row g-3">
                            <div class="col-md-4">
                                <label class="form-label">Catégorie</label>
                                <select class="form-select" id="category-filter">
                                    <option value="">Toutes les catégories</option>
                                    <option value="ELECTRONIQUE">Électronique</option>
                                    <option value="ALIMENTAIRE">Alimentaire</option>
                                    <option value="VETEMENT">Vêtement</option>
                                    <option value="AUTRE">Autre</option>
                                </select>
                            </div>
                            <div class="col-md-4">
                                <label class="form-label">État du Stock</label>
                                <select class="form-select" id="stock-filter">
                                    <option value="">Tous les états</option>
                                    <option value="disponible">Disponible</option>
                                    <option value="faible">Stock Faible</option>
                                    <option value="critique">Stock Critique</option>
                                    <option value="rupture">Rupture</option>
                                </select>
                            </div>
                            <div class="col-md-4">
                                <label class="form-label">Fourchette de Prix (DH)</label>
                                <div class="d-flex gap-2">
                                    <input type="number" class="form-control" placeholder="Min" id="price-min">
                                    <input type="number" class="form-control" placeholder="Max" id="price-max">
                                </div>
                            </div>
                        </div>
                        <div class="mt-3">
                            <button class="btn btn-primary" onclick="advancedSearch.applyFilters()">
                                <i class="fas fa-filter me-2"></i>Appliquer les Filtres
                            </button>
                            <button class="btn btn-outline-secondary ms-2" onclick="advancedSearch.clearFilters()">
                                <i class="fas fa-times me-2"></i>Effacer
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Résultats de Recherche -->
                <div class="search-results" id="search-results" style="display: none;">
                    <h5><i class="fas fa-list me-2"></i>Résultats de la Recherche</h5>
                    <div id="results-container"></div>
                </div>
            </div>
        `;
    }

    bindEvents() {
        // Gestion des onglets
        document.querySelectorAll('.search-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });

        // Recherche en temps réel
        const textSearch = document.getElementById('text-search');
        if (textSearch) {
            textSearch.addEventListener('input', (e) => {
                if (e.target.value.length > 2) {
                    this.performTextSearch();
                }
            });
        }

        // Scanner simulation
        const scannerArea = document.getElementById('scanner-area');
        if (scannerArea) {
            scannerArea.addEventListener('click', () => {
                if (this.isScanning) {
                    this.simulateBarcodeScan();
                }
            });
        }
    }

    switchTab(tabName) {
        // Mise à jour des onglets
        document.querySelectorAll('.search-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Affichage du panneau correspondant
        document.querySelectorAll('.search-panel').forEach(panel => {
            panel.style.display = 'none';
        });
        document.getElementById(`${tabName}-panel`).style.display = 'block';

        this.currentTab = tabName;
    }

    async performTextSearch() {
        const query = document.getElementById('text-search').value;
        if (!query || query.length < 2) return;

        try {
            const response = await fetch(`/articles/search/?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            this.displayResults(data.results || []);
        } catch (error) {
            console.error('Erreur de recherche:', error);
            this.showNotification('Erreur lors de la recherche', 'error');
        }
    }

    toggleScanner() {
        this.isScanning = !this.isScanning;
        const btnText = document.getElementById('scanner-btn-text');
        const scannerLine = document.getElementById('scanner-line');
        const scannerText = document.getElementById('scanner-text');

        if (this.isScanning) {
            btnText.textContent = 'Arrêter le Scanner';
            scannerLine.style.display = 'block';
            scannerText.textContent = 'Scanner actif - Cliquez pour simuler';
            scannerText.style.animation = 'pulse 1s infinite';
        } else {
            btnText.textContent = 'Démarrer le Scanner';
            scannerLine.style.display = 'none';
            scannerText.textContent = 'Cliquez pour simuler un scan';
            scannerText.style.animation = 'none';
        }
    }

    simulateBarcodeScan() {
        // Simulation de codes-barres aléatoires
        const mockBarcodes = [
            '1234567890123',
            '9876543210987',
            '5555666677778',
            '1111222233334',
            '9999888877776'
        ];

        const randomBarcode = mockBarcodes[Math.floor(Math.random() * mockBarcodes.length)];
        
        // Animation de scan
        this.showScanAnimation();
        
        setTimeout(() => {
            this.searchByBarcode(randomBarcode);
        }, 1500);
    }

    showScanAnimation() {
        const scannerText = document.getElementById('scanner-text');
        scannerText.innerHTML = `
            <div class="shimmer">Scanning...</div>
            <div style="font-size: 0.8rem; margin-top: 0.5rem;">
                <i class="fas fa-spinner fa-spin"></i> Lecture en cours...
            </div>
        `;
    }

    async searchByBarcode(barcode) {
        try {
            // Simulation de recherche par code-barres
            const mockResults = [
                {
                    id: 1,
                    nom: 'Article Scanné',
                    reference: barcode,
                    stock_disponible: Math.floor(Math.random() * 100),
                    prix: (Math.random() * 1000).toFixed(2)
                }
            ];

            document.getElementById('scanner-text').innerHTML = `
                <div style="color: var(--green-400);">
                    <i class="fas fa-check-circle"></i> Code-barres détecté !
                </div>
                <div style="font-size: 0.9rem; margin-top: 0.5rem;">
                    ${barcode}
                </div>
            `;

            this.displayResults(mockResults);
            this.showNotification(`Article trouvé avec le code-barres: ${barcode}`, 'success');
        } catch (error) {
            this.showNotification('Aucun article trouvé avec ce code-barres', 'warning');
        }
    }

    quickFilter(type) {
        // Activation visuelle du filtre
        document.querySelectorAll('.filter-chip').forEach(chip => {
            chip.classList.remove('active');
        });
        event.target.classList.add('active');

        // Application du filtre rapide
        this.applyQuickFilter(type);
    }

    async applyQuickFilter(type) {
        let url = '/articles/';
        switch (type) {
            case 'stock_critique':
                url += '?stock_status=critique';
                break;
            case 'nouveaux':
                url += '?sort=newest';
                break;
            case 'populaires':
                url += '?sort=popular';
                break;
        }

        try {
            const response = await fetch(url);
            const data = await response.json();
            this.displayResults(data.results || []);
        } catch (error) {
            console.error('Erreur de filtrage:', error);
        }
    }

    displayResults(results) {
        const resultsContainer = document.getElementById('results-container');
        const searchResults = document.getElementById('search-results');

        if (!results || results.length === 0) {
            resultsContainer.innerHTML = `
                <div class="text-center py-4 text-muted">
                    <i class="fas fa-search fa-3x mb-3"></i>
                    <p>Aucun résultat trouvé</p>
                </div>
            `;
        } else {
            resultsContainer.innerHTML = results.map(item => `
                <div class="result-item scale-in" onclick="advancedSearch.selectItem(${item.id})">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="mb-1">${item.nom}</h6>
                            <small class="text-muted">Réf: ${item.reference}</small>
                        </div>
                        <div class="text-end">
                            <div class="badge bg-primary">${item.stock_disponible} unités</div>
                            <div class="text-success fw-bold">${item.prix} DH</div>
                        </div>
                    </div>
                </div>
            `).join('');
        }

        searchResults.style.display = 'block';
    }

    selectItem(itemId) {
        // Redirection vers la page de détail de l'article
        window.location.href = `/articles/${itemId}/`;
    }

    showNotification(message, type = 'info') {
        // Utilisation du système de notifications existant
        if (window.notificationSystem) {
            window.notificationSystem.showNotification('Recherche', message, type, 3000);
        } else {
            alert(message);
        }
    }

    initBarcodeScanner() {
        // Initialisation du scanner (simulation)
        console.log('Scanner de codes-barres initialisé (mode simulation)');
    }
}

// Initialisation automatique
document.addEventListener('DOMContentLoaded', function() {
    window.advancedSearch = new AdvancedSearch();
});
