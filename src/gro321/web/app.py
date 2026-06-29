"""
Application web minimaliste pour le système GMAO.
Utilise uniquement la bibliothèque standard (http.server).
"""

import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Ajouter le chemin src au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gro321.database import (
    creer_bon_diagnostic,
    creer_bon_mise_a_jour,
    creer_bon_reparation,
    creer_client,
    creer_robot,
    get_connection,
    lire_bon,
    lister_bons,
    modifier_client,
    modifier_robot,
    modifier_statut_bon,
    supprimer_client,
    supprimer_robot,
)

# NOTE POUR LES ÉTUDIANTS:
# La couche web des bons de travail est complete et active (routes, methodes et
# formulaire). Il vous reste a implementer la logique d'acces aux donnees dans
# crud_bons.py (et la hierarchie de classes dans bon_travail.py). Tant que ces
# fonctions renvoient None, la creation et la lecture de bons resteront sans
# effet; elles fonctionneront automatiquement une fois crud_bons.py complete.


class GMaoRequestHandler(BaseHTTPRequestHandler):
    """Gestionnaire de requêtes HTTP pour l'application GMAO."""

    def do_GET(self):
        """Traite les requêtes GET."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == "/" or path == "/index.html":
            self.serve_index()
        elif path == "/api/bons":
            self.api_lister_bons()
        elif path == "/api/robots":
            self.api_lister_robots()
        elif path == "/api/clients":
            self.api_lister_clients()
        elif path.startswith("/api/bon/"):
            bon_id = path.split("/")[-1]
            self.api_obtenir_bon(bon_id)
        else:
            self.send_error(404, "Page non trouvée")

    def do_POST(self):
        """Traite les requêtes POST."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode("utf-8"))

        if path == "/api/bon/diagnostic":
            self.api_creer_bon_diagnostic(data)
        elif path == "/api/bon/mise_a_jour":
            self.api_creer_bon_mise_a_jour(data)
        elif path == "/api/bon/reparation":
            self.api_creer_bon_reparation(data)
        elif path == "/api/bon/statut":
            self.api_modifier_statut(data)
        elif path == "/api/client":
            self.api_creer_client(data)
        elif path == "/api/client/modifier":
            self.api_modifier_client(data)
        elif path == "/api/client/supprimer":
            self.api_supprimer_client(data)
        elif path == "/api/robot":
            self.api_creer_robot(data)
        elif path == "/api/robot/modifier":
            self.api_modifier_robot(data)
        elif path == "/api/robot/supprimer":
            self.api_supprimer_robot(data)
        else:
            self.send_error(404, "Point d'accès non trouvé")

    def serve_index(self):
        """Sert la page HTML principale."""
        html = self.get_html_page()
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def api_lister_bons(self):
        """API: Liste tous les bons de travail."""
        bons = lister_bons()
        self.send_json_response(bons)

    def api_lister_robots(self):
        """API: Liste tous les robots avec le nom de leur client."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.robot_id, r.modele, r.numero_serie, r.statut,
                       c.nom as nom_client
                FROM robots r
                JOIN clients c ON r.client_id = c.client_id
                ORDER BY r.robot_id
            """)
            robots = [dict(row) for row in cursor.fetchall()]

        self.send_json_response(robots)

    def api_lister_clients(self):
        """API: Liste tous les clients."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients ORDER BY nom")
            clients = [dict(row) for row in cursor.fetchall()]

        self.send_json_response(clients)

    def api_obtenir_bon(self, bon_id):
        """API: Obtient les détails d'un bon."""
        try:
            bon = lire_bon(int(bon_id))
            if bon:
                self.send_json_response(
                    {
                        "bon_id": bon.bon_id,
                        "numero_serie": bon.numero_serie,
                        "type_bon": bon.type_bon,
                        "statut": bon.statut,
                        "description": bon.obtenir_description(),
                    }
                )
            else:
                self.send_error(404, "Bon non trouvé")
        except Exception as e:
            self.send_error(500, str(e))

    def api_creer_bon_diagnostic(self, data):
        """API: Crée un bon de diagnostic."""
        try:
            bon_id = creer_bon_diagnostic(
                numero_serie=data["numero_serie"], symptomes=data["symptomes"]
            )
            self.send_json_response({"bon_id": bon_id, "success": True})
        except Exception as e:
            self.send_error(500, str(e))

    def api_creer_bon_mise_a_jour(self, data):
        """API: Crée un bon de mise à jour."""
        try:
            bon_id = creer_bon_mise_a_jour(
                numero_serie=data["numero_serie"],
                version_actuelle=data["version_actuelle"],
                version_cible=data["version_cible"],
            )
            self.send_json_response({"bon_id": bon_id, "success": True})
        except Exception as e:
            self.send_error(500, str(e))

    def api_creer_bon_reparation(self, data):
        """API: Crée un bon de réparation."""
        try:
            bon_id = creer_bon_reparation(
                numero_serie=data["numero_serie"],
                composant=data["composant"],
                probleme=data["probleme"],
            )
            self.send_json_response({"bon_id": bon_id, "success": True})
        except Exception as e:
            self.send_error(500, str(e))

    def api_modifier_statut(self, data):
        """API: Modifie le statut d'un bon."""
        try:
            success = modifier_statut_bon(data["bon_id"], data["statut"])
            self.send_json_response({"success": success})
        except Exception as e:
            self.send_error(500, str(e))

    def api_creer_client(self, data):
        """API: Crée un nouveau client."""
        try:
            client_id = creer_client(
                nom=data["nom"], contact=data["contact"], adresse=data["adresse"]
            )
            self.send_json_response({"client_id": client_id, "success": True})
        except Exception as e:
            self.send_error(500, str(e))

    def api_modifier_client(self, data):
        """API: Modifie un client."""
        try:
            success = modifier_client(
                client_id=data["client_id"],
                nom=data.get("nom"),
                contact=data.get("contact"),
                adresse=data.get("adresse"),
            )
            self.send_json_response({"success": success})
        except Exception as e:
            self.send_error(500, str(e))

    def api_supprimer_client(self, data):
        """API: Supprime un client."""
        try:
            success = supprimer_client(data["client_id"])
            self.send_json_response({"success": success})
        except Exception as e:
            self.send_error(500, str(e))

    def api_creer_robot(self, data):
        """API: Crée un nouveau robot."""
        try:
            robot_id = creer_robot(
                modele=data["modele"],
                numero_serie=data["numero_serie"],
                client_id=data["client_id"],
                statut=data.get("statut", "operationnel"),
            )
            self.send_json_response({"robot_id": robot_id, "success": True})
        except Exception as e:
            self.send_error(500, str(e))

    def api_modifier_robot(self, data):
        """API: Modifie un robot."""
        try:
            success = modifier_robot(
                robot_id=data["robot_id"],
                modele=data.get("modele"),
                statut=data.get("statut"),
                client_id=data.get("client_id"),
            )
            self.send_json_response({"success": success})
        except Exception as e:
            self.send_error(500, str(e))

    def api_supprimer_robot(self, data):
        """API: Supprime un robot."""
        try:
            success = supprimer_robot(data["robot_id"])
            self.send_json_response({"success": success})
        except Exception as e:
            self.send_error(500, str(e))

    def send_json_response(self, data):
        """Envoie une réponse JSON."""
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def get_html_page(self):
        """Retourne le code HTML de la page principale."""
        return HTML_PAGE

    def log_message(self, format, *args):
        """Surcharge pour formater les journaux."""
        print(f"[{self.log_date_time_string()}] {format % args}")


HTML_PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GMAO - Système de Gestion de Maintenance</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto;
               padding: 20px; background-color: #f5f5f5; }
        h1, h2 { color: #333; }
        h3 { color: #555; margin-top: 20px; }
        .section { background: white; padding: 20px; margin: 20px 0;
                   border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #f8f8f8; }
        button { background-color: #4CAF50; color: white; padding: 10px 20px;
                 border: none; border-radius: 4px; cursor: pointer; margin: 5px 5px 5px 0; }
        button:hover { background-color: #45a049; }
        button.danger { background-color: #f44336; }
        button.danger:hover { background-color: #d32f2f; }
        .form-group { margin: 10px 0; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select, textarea { width: 100%; padding: 8px; border: 1px solid #ddd;
                                  border-radius: 4px; box-sizing: border-box; }
        textarea { min-height: 80px; }
        .status-ouvert { color: #ff9800; }
        .status-en_cours { color: #2196F3; }
        .status-termine { color: #4CAF50; }
        .status-annule { color: #f44336; }
    </style>
</head>
<body>
    <h1>Système de Gestion de Maintenance (GMAO)</h1>

    <div class="section">
        <h2>Bons de Travail</h2>
        <button onclick="rafraichirBons()">Rafraîchir</button>
        <table id="tableBons">
            <thead>
                <tr><th>ID</th><th>Robot (no de série)</th><th>Type</th><th>Date</th><th>Statut</th></tr>
            </thead>
            <tbody></tbody>
        </table>
    </div>

    <div class="section">
        <h2>Créer un Bon de Travail</h2>
        <div class="form-group">
            <label>Type de bon:</label>
            <select id="typeBon" onchange="afficherFormulaire()">
                <option value="">-- Sélectionnez --</option>
                <option value="diagnostic">Diagnostic</option>
                <option value="mise_a_jour">Mise à jour</option>
                <option value="reparation">Réparation</option>
            </select>
        </div>
        <div id="formBon" style="display:none;">
            <div class="form-group">
                <label>Robot:</label>
                <select id="numeroSerie"></select>
            </div>
            <div id="champsSpecifiques"></div>
            <button onclick="creerBon()">Créer le bon</button>
        </div>
    </div>

    <div class="section">
        <h2>Robots</h2>
        <table id="tableRobots">
            <thead>
                <tr><th>ID</th><th>Modèle</th><th>Numéro de série</th><th>Client</th><th>Statut</th></tr>
            </thead>
            <tbody></tbody>
        </table>

        <h3>Ajouter un robot</h3>
        <div class="form-group"><label>Modèle:</label><input type="text" id="robModele"></div>
        <div class="form-group"><label>Numéro de série:</label><input type="text" id="robSerie"></div>
        <div class="form-group"><label>Client:</label><select id="robClient"></select></div>
        <div class="form-group"><label>Statut:</label>
            <select id="robStatut">
                <option value="operationnel">operationnel</option>
                <option value="en_maintenance">en_maintenance</option>
                <option value="hors_service">hors_service</option>
            </select>
        </div>
        <button onclick="ajouterRobot()">Ajouter le robot</button>

        <h3>Modifier ou supprimer un robot</h3>
        <div class="form-group"><label>ID du robot:</label><input type="number" id="robId"></div>
        <div class="form-group"><label>Nouveau modèle (laisser vide si inchangé):</label><input type="text" id="robModeleU"></div>
        <div class="form-group"><label>Nouveau statut (laisser vide si inchangé):</label>
            <select id="robStatutU">
                <option value="">-- inchangé --</option>
                <option value="operationnel">operationnel</option>
                <option value="en_maintenance">en_maintenance</option>
                <option value="hors_service">hors_service</option>
            </select>
        </div>
        <div class="form-group"><label>Nouveau client (laisser vide si inchangé):</label><select id="robClientU"></select></div>
        <button onclick="modifierRobot()">Modifier</button>
        <button class="danger" onclick="supprimerRobot()">Supprimer</button>
    </div>

    <div class="section">
        <h2>Clients</h2>
        <table id="tableClients">
            <thead>
                <tr><th>ID</th><th>Nom</th><th>Contact</th><th>Adresse</th></tr>
            </thead>
            <tbody></tbody>
        </table>

        <h3>Ajouter un client</h3>
        <div class="form-group"><label>Nom:</label><input type="text" id="cltNom"></div>
        <div class="form-group"><label>Contact:</label><input type="text" id="cltContact"></div>
        <div class="form-group"><label>Adresse:</label><input type="text" id="cltAdresse"></div>
        <button onclick="ajouterClient()">Ajouter le client</button>

        <h3>Modifier ou supprimer un client</h3>
        <div class="form-group"><label>ID du client:</label><input type="number" id="cltId"></div>
        <div class="form-group"><label>Nouveau nom (laisser vide si inchangé):</label><input type="text" id="cltNomU"></div>
        <div class="form-group"><label>Nouveau contact (laisser vide si inchangé):</label><input type="text" id="cltContactU"></div>
        <div class="form-group"><label>Nouvelle adresse (laisser vide si inchangé):</label><input type="text" id="cltAdresseU"></div>
        <button onclick="modifierClient()">Modifier</button>
        <button class="danger" onclick="supprimerClient()">Supprimer</button>
    </div>

    <script>
        function postJSON(url, data) {
            return fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            }).then(r => r.json());
        }

        function rafraichirBons() {
            fetch('/api/bons').then(r => r.json()).then(bons => {
                const tbody = document.querySelector('#tableBons tbody');
                tbody.innerHTML = '';
                bons.forEach(bon => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `<td>${bon.bon_id}</td><td>${bon.numero_serie}</td>` +
                        `<td>${bon.type_bon}</td><td>${bon.date_creation}</td>` +
                        `<td class="status-${bon.statut}">${bon.statut}</td>`;
                    tbody.appendChild(tr);
                });
            });
        }

        function chargerRobots() {
            fetch('/api/robots').then(r => r.json()).then(robots => {
                const select = document.getElementById('numeroSerie');
                select.innerHTML = '<option value="">-- Sélectionnez --</option>';
                robots.forEach(robot => {
                    const opt = document.createElement('option');
                    opt.value = robot.numero_serie;
                    opt.textContent = `${robot.numero_serie} - ${robot.modele} (${robot.nom_client})`;
                    select.appendChild(opt);
                });
                const tbody = document.querySelector('#tableRobots tbody');
                tbody.innerHTML = '';
                robots.forEach(robot => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `<td>${robot.robot_id}</td><td>${robot.modele}</td>` +
                        `<td>${robot.numero_serie}</td><td>${robot.nom_client}</td>` +
                        `<td>${robot.statut}</td>`;
                    tbody.appendChild(tr);
                });
            });
        }

        function chargerClients() {
            fetch('/api/clients').then(r => r.json()).then(clients => {
                const tbody = document.querySelector('#tableClients tbody');
                tbody.innerHTML = '';
                clients.forEach(client => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `<td>${client.client_id}</td><td>${client.nom}</td>` +
                        `<td>${client.contact}</td><td>${client.adresse}</td>`;
                    tbody.appendChild(tr);
                });
                const opts = '<option value="">-- Sélectionnez --</option>' +
                    clients.map(c => `<option value="${c.client_id}">${c.client_id} - ${c.nom}</option>`).join('');
                document.getElementById('robClient').innerHTML = opts;
                document.getElementById('robClientU').innerHTML =
                    '<option value="">-- inchangé --</option>' +
                    clients.map(c => `<option value="${c.client_id}">${c.client_id} - ${c.nom}</option>`).join('');
            });
        }

        function rafraichirTout() {
            rafraichirBons();
            chargerRobots();
            chargerClients();
        }

        function afficherFormulaire() {
            const type = document.getElementById('typeBon').value;
            const form = document.getElementById('formBon');
            const champs = document.getElementById('champsSpecifiques');
            if (!type) { form.style.display = 'none'; return; }
            form.style.display = 'block';
            if (type === 'diagnostic') {
                champs.innerHTML = '<div class="form-group"><label>Symptômes:</label>' +
                    '<textarea id="symptomes"></textarea></div>';
            } else if (type === 'mise_a_jour') {
                champs.innerHTML = '<div class="form-group"><label>Version actuelle:</label>' +
                    '<input type="text" id="versionActuelle" /></div>' +
                    '<div class="form-group"><label>Version cible:</label>' +
                    '<input type="text" id="versionCible" /></div>';
            } else if (type === 'reparation') {
                champs.innerHTML = '<div class="form-group"><label>Composant:</label>' +
                    '<input type="text" id="composant" /></div>' +
                    '<div class="form-group"><label>Problème:</label>' +
                    '<textarea id="probleme"></textarea></div>';
            }
        }

        function creerBon() {
            const type = document.getElementById('typeBon').value;
            const numeroSerie = document.getElementById('numeroSerie').value;
            if (!numeroSerie) { alert('Veuillez sélectionner un robot'); return; }
            let url = '';
            let data = { numero_serie: numeroSerie };
            if (type === 'diagnostic') {
                url = '/api/bon/diagnostic';
                data.symptomes = document.getElementById('symptomes').value;
            } else if (type === 'mise_a_jour') {
                url = '/api/bon/mise_a_jour';
                data.version_actuelle = document.getElementById('versionActuelle').value;
                data.version_cible = document.getElementById('versionCible').value;
            } else if (type === 'reparation') {
                url = '/api/bon/reparation';
                data.composant = document.getElementById('composant').value;
                data.probleme = document.getElementById('probleme').value;
            }
            postJSON(url, data).then(result => {
                alert('Bon créé avec succès (ID: ' + result.bon_id + ')');
                rafraichirBons();
                document.getElementById('typeBon').value = '';
                afficherFormulaire();
            }).catch(err => alert('Erreur: ' + err));
        }

        function ajouterClient() {
            const data = {
                nom: document.getElementById('cltNom').value,
                contact: document.getElementById('cltContact').value,
                adresse: document.getElementById('cltAdresse').value
            };
            if (!data.nom) { alert('Le nom est requis'); return; }
            postJSON('/api/client', data).then(() => {
                alert('Client ajouté');
                chargerClients();
            }).catch(err => alert('Erreur: ' + err));
        }

        function modifierClient() {
            const id = document.getElementById('cltId').value;
            if (!id) { alert('ID du client requis'); return; }
            const data = { client_id: parseInt(id) };
            const nom = document.getElementById('cltNomU').value;
            const contact = document.getElementById('cltContactU').value;
            const adresse = document.getElementById('cltAdresseU').value;
            if (nom) data.nom = nom;
            if (contact) data.contact = contact;
            if (adresse) data.adresse = adresse;
            postJSON('/api/client/modifier', data).then(() => {
                alert('Client modifié');
                chargerClients();
            }).catch(err => alert('Erreur: ' + err));
        }

        function supprimerClient() {
            const id = document.getElementById('cltId').value;
            if (!id) { alert('ID du client requis'); return; }
            postJSON('/api/client/supprimer', { client_id: parseInt(id) }).then(() => {
                alert('Client supprimé');
                rafraichirTout();
            }).catch(err => alert('Erreur: ' + err));
        }

        function ajouterRobot() {
            const data = {
                modele: document.getElementById('robModele').value,
                numero_serie: document.getElementById('robSerie').value,
                client_id: parseInt(document.getElementById('robClient').value),
                statut: document.getElementById('robStatut').value
            };
            if (!data.modele || !data.numero_serie || !data.client_id) {
                alert('Modèle, numéro de série et client sont requis'); return;
            }
            postJSON('/api/robot', data).then(() => {
                alert('Robot ajouté');
                chargerRobots();
            }).catch(err => alert('Erreur: ' + err));
        }

        function modifierRobot() {
            const id = document.getElementById('robId').value;
            if (!id) { alert('ID du robot requis'); return; }
            const data = { robot_id: parseInt(id) };
            const modele = document.getElementById('robModeleU').value;
            const statut = document.getElementById('robStatutU').value;
            const client = document.getElementById('robClientU').value;
            if (modele) data.modele = modele;
            if (statut) data.statut = statut;
            if (client) data.client_id = parseInt(client);
            postJSON('/api/robot/modifier', data).then(() => {
                alert('Robot modifié');
                chargerRobots();
            }).catch(err => alert('Erreur: ' + err));
        }

        function supprimerRobot() {
            const id = document.getElementById('robId').value;
            if (!id) { alert('ID du robot requis'); return; }
            postJSON('/api/robot/supprimer', { robot_id: parseInt(id) }).then(() => {
                alert('Robot supprimé');
                rafraichirTout();
            }).catch(err => alert('Erreur: ' + err));
        }

        rafraichirTout();
    </script>
</body>
</html>
"""


def main():
    """Point d'entrée principal de l'application."""
    host = "127.0.0.1"
    port = 18000

    print(f"Démarrage du serveur GMAO sur http://{host}:{port}")
    print("Appuyez sur Ctrl+C pour arrêter")

    server = HTTPServer((host, port), GMaoRequestHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nArrêt du serveur...")
        server.shutdown()


if __name__ == "__main__":
    main()
