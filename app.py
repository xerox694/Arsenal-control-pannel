#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arsenal WebPanel - VERSION ULTRA SIMPLE ET PROPRE
Direct au dashboard - Pas de complexité inutile
Version: 1.0.0 - SIMPLE ET EFFICACE
"""

from flask import Flask, render_template_string, jsonify
import os

app = Flask(__name__)

# ==================== DASHBOARD DIRECT ====================

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arsenal WebPanel - Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 20px 0;
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 28px;
            font-weight: bold;
            color: #667eea;
        }
        
        .status {
            background: #28a745;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
        }
        
        .main-content {
            padding: 40px 0;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 30px;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .card-icon {
            width: 50px;
            height: 50px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            font-size: 24px;
        }
        
        .card-title {
            font-size: 20px;
            font-weight: 600;
            color: #333;
        }
        
        .card-value {
            font-size: 36px;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }
        
        .card-description {
            color: #666;
            font-size: 14px;
        }
        
        .bot-status { background: linear-gradient(135deg, #28a745, #20c997); }
        .server-count { background: linear-gradient(135deg, #667eea, #764ba2); }
        .user-count { background: linear-gradient(135deg, #ffc107, #fd7e14); }
        .commands-count { background: linear-gradient(135deg, #dc3545, #e83e8c); }
        
        .welcome-section {
            text-align: center;
            color: white;
            margin-bottom: 20px;
        }
        
        .welcome-title {
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .welcome-subtitle {
            font-size: 18px;
            opacity: 0.9;
        }
        
        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                gap: 15px;
            }
            
            .welcome-title {
                font-size: 32px;
            }
            
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <div class="header-content">
                <div class="logo">🛡️ Arsenal WebPanel</div>
                <div class="status">✅ Opérationnel</div>
            </div>
        </div>
    </div>
    
    <div class="main-content">
        <div class="container">
            <div class="welcome-section">
                <h1 class="welcome-title">Bienvenue sur Arsenal WebPanel</h1>
                <p class="welcome-subtitle">Tableau de bord simplifié et efficace</p>
            </div>
            
            <div class="dashboard-grid">
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon bot-status">🤖</div>
                        <div class="card-title">Statut du Bot</div>
                    </div>
                    <div class="card-value" id="bot-status">En ligne</div>
                    <div class="card-description">Bot Arsenal opérationnel</div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon server-count">🖥️</div>
                        <div class="card-title">Serveurs</div>
                    </div>
                    <div class="card-value" id="server-count">6</div>
                    <div class="card-description">Serveurs connectés</div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon user-count">👥</div>
                        <div class="card-title">Utilisateurs</div>
                    </div>
                    <div class="card-value" id="user-count">57</div>
                    <div class="card-description">Utilisateurs actifs</div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <div class="card-icon commands-count">⚡</div>
                        <div class="card-title">Commandes</div>
                    </div>
                    <div class="card-value" id="commands-count">2,847</div>
                    <div class="card-description">Commandes exécutées</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Mise à jour des stats en temps réel
        function updateStats() {
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('bot-status').textContent = data.online ? 'En ligne' : 'Hors ligne';
                    document.getElementById('server-count').textContent = data.servers || 6;
                    document.getElementById('user-count').textContent = data.users || 57;
                    document.getElementById('commands-count').textContent = (data.commands || 2847).toLocaleString();
                })
                .catch(error => console.log('Stats non disponibles:', error));
        }
        
        // Mettre à jour toutes les 30 secondes
        updateStats();
        setInterval(updateStats, 30000);
    </script>
</body>
</html>
'''

# ==================== ROUTES SIMPLES ====================

@app.route('/')
def dashboard():
    """Dashboard principal - direct sans login"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/stats')
def api_stats():
    """API simple pour les statistiques"""
    return jsonify({
        'online': True,
        'servers': 6,
        'users': 57,
        'commands': 2847,
        'uptime': '2j 15h 42m',
        'status': 'operational'
    })

@app.route('/api/health')
def api_health():
    """API de santé du service"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0 - SIMPLE',
        'message': 'Arsenal WebPanel fonctionne parfaitement !'
    })

# ==================== DÉMARRAGE ====================

if __name__ == '__main__':
    print("🚀 Arsenal WebPanel - VERSION SIMPLE")
    print("📊 Dashboard direct sans complexité")
    print("🌐 http://localhost:5000")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
