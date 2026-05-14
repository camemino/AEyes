# Suivi de projet V3 — A-Eyes

## Contexte

V3 : ajout de fonctionnalités statiques à l'application.
- Suppression du bouton SCAN (caméra ouverte par défaut).
- Nouvelle feature **Text** (OCR — détection et lecture du texte visible).

---

## Phases d'implémentation

### Phase 1 — Suppression du bouton SCAN

| Fichier | Changement | Statut |
|---------|-----------|--------|
| `frontend/index.html` | Suppression `<button id="btn-scan">` | ✅ |
| `frontend/js/app.js` | Suppression `this._btnScan`, `this._scanning`, `toggleScan()` | ✅ |
| `frontend/js/app.js` | `_enterMain()` appelle `_startCamera()` au démarrage | ✅ |
| `frontend/js/app.js` | `_stopCamera()` utilise `this._cam.isOpen` (plus de ref btnScan) | ✅ |
| `frontend/js/app.js` | Retrait commande vocale 'scan' de `_handleCommand()` | ✅ |
| `frontend/js/voice.js` | Retrait `scan` de la table `COMMANDS` | ✅ |
| `frontend/css/style.css` | Suppression du bloc `.btn-scan` | ✅ |

### Phase 2 — Feature Text (OCR)

| Fichier | Changement | Statut |
|---------|-----------|--------|
| `backend/api/text.py` | Nouveau endpoint `POST /api/text` (OCR GPT-4.1-mini) | ✅ |
| `backend/main.py` | Import et inclusion du router `text_router` | ✅ |
| `frontend/index.html` | Ajout `<button id="btn-text">TEXT</button>` | ✅ |
| `frontend/js/app.js` | Ajout `onText()`, listener btn-text | ✅ |
| `frontend/js/app.js` | Ajout commande vocale 'text' dans `_handleCommand()` | ✅ |
| `frontend/js/voice.js` | Ajout `text` dans la table `COMMANDS` | ✅ |
| `frontend/css/style.css` | Ajout `.btn-text { background: #FF8C00; }` | ✅ |

### Phase 3 — Documentation V3

| Fichier | Contenu | Statut |
|---------|---------|--------|
| `Docs/V3/architecture_V3.md` | Architecture mise à jour, diagrammes de séquence, endpoint `/api/text` | ✅ |
| `Docs/V3/fonctionnalites_V3.md` | Rationale UX, feature Text, scénario Ahmed, tableau de comparaison | ✅ |
| `Docs/V3/suivi_projet_V3.md` | Ce document | ✅ |

---

## Tableau de vérification

| Test | Attendu | Statut |
|------|---------|--------|
| Ouverture de l'app | Caméra démarre sans clic, TTS "A-Eyes ready..." | À tester |
| Permission caméra refusée | TTS "Camera unavailable. Please check permissions." | À tester |
| Clic bouton DESCRIBE | TTS "Analysing scene..." → description de la scène | À tester |
| Clic bouton TEXT (texte visible) | TTS "Reading text..." → texte détecté dicté | À tester |
| Clic bouton TEXT (pas de texte) | TTS "No text detected in the image." | À tester |
| Commande vocale "text" | Même comportement que clic bouton TEXT | À tester |
| Commande vocale "describe" | Même comportement que clic bouton DESCRIBE | À tester |
| Commande vocale "help" | TTS "Available commands: describe, text, repeat, settings, stop." | À tester |
| Commande vocale "stop" | Caméra s'arrête, TTS "Camera off." | À tester |
| Bouton REPEAT | Relit le dernier message | À tester |
| Bouton SETTINGS → slider → BACK | Vitesse TTS mise à jour, retour écran principal + caméra auto | À tester |
| `POST /api/text` via Swagger `/docs` | JSON `{"text": "..."}` retourné | À tester |

---

## Problèmes connus

| ID | Description | Priorité |
|----|-------------|----------|
| P-01 | La caméra se ferme si l'utilisateur navigue vers SETTINGS puis revient (comportement attendu, mais peut surprendre) | Faible |
| P-02 | Sur Firefox, Web Speech API non supportée — les boutons restent fonctionnels mais les commandes vocales sont désactivées | Faible |
| P-03 | Si la clé OpenAI est épuisée ou invalide, les deux endpoints retournent un message d'erreur vocal au lieu de planter silencieusement | Documenté |

---

## Feuille de route V4 (à planifier)

- PWA (Progressive Web App) : installation sur l'écran d'accueil mobile, mode hors-ligne partiel.
- Internationalisation : détection de langue du texte OCR, adaptation de la voix TTS.
- Historique vocal : navigation dans les dernières descriptions dictées.
- Mode nuit automatique : réduction de la consommation de batterie (caméra basse résolution).
