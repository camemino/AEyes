# Suivi de projet V3 — A-Eyes

## Contexte

V3 : améliorations de l'expérience utilisateur et nouvelles fonctionnalités.

---

## Phases d'implémentation

### Phase 1 — Suppression du bouton SCAN

| Fichier | Changement | Statut |
|---------|-----------|--------|
| `frontend/index.html` | Suppression `<button id="btn-scan">` | ✅ |
| `frontend/js/app.js` | Suppression `toggleScan()`, caméra auto dans `_enterMain()` | ✅ |
| `frontend/js/voice.js` | Retrait `scan` de la table `COMMANDS` | ✅ |
| `frontend/css/style.css` | Suppression bloc `.btn-scan` | ✅ |

### Phase 2 — Feature Text (OCR)

| Fichier | Changement | Statut |
|---------|-----------|--------|
| `backend/api/text.py` | Nouveau endpoint `POST /api/text` | ✅ |
| `backend/main.py` | Import et inclusion de `text_router` | ✅ |
| `frontend/index.html` | Ajout `<button id="btn-text">` | ✅ |
| `frontend/js/app.js` | Ajout `onText()`, listener btn-text, commande vocale | ✅ |
| `frontend/js/voice.js` | Ajout `text` dans `COMMANDS` | ✅ |
| `frontend/css/style.css` | Ajout `.btn-text { background: #FF8C00 }` | ✅ |

### Phase 3 — Feature Details

| Fichier | Changement | Statut |
|---------|-----------|--------|
| `backend/api/details.py` | Nouveau endpoint `POST /api/details` (2-3 phrases, max_tokens: 500) | ✅ |
| `backend/main.py` | Import et inclusion de `details_router` | ✅ |
| `frontend/index.html` | Ajout `<button id="btn-details">` | ✅ |
| `frontend/js/app.js` | Ajout `onDetails()` (utilise `_lastFrame`, pas de capture) | ✅ |
| `frontend/js/voice.js` | Ajout `details` dans `COMMANDS` | ✅ |
| `frontend/css/style.css` | Ajout `.btn-details { background: #0a7a3e }` | ✅ |

### Phase 4 — Suppression de l'écran Settings

| Fichier | Changement | Statut |
|---------|-----------|--------|
| `frontend/index.html` | Suppression bouton SETTINGS et section `#settings-screen` | ✅ |
| `frontend/js/app.js` | Suppression `goToSettings()`, `goBack()`, `onRateChange()`, `_leaveMain()` | ✅ |
| `frontend/js/voice.js` | Retrait `settings` de `COMMANDS` | ✅ |
| `frontend/css/style.css` | Suppression `.btn-settings`, `.btn-back`, styles `#settings-screen` | ✅ |

### Phase 5 — Anti-boucle vocale TTS (solution finale)

| Fichier | Changement | Statut |
|---------|-----------|--------|
| `frontend/js/voice.js` | Ajout `startListening()` / `stopListening()` | ✅ |
| `frontend/js/tts.js` | Refactorisation — `speak(text, onEnd)` avec callback direct, `u.onerror` fallback Chrome | ✅ |
| `frontend/js/app.js` | `_setBusy()` → `stopListening()` ; `_setIdle()` → `startListening()` dans callback TTS final | ✅ |
| `frontend/js/app.js` | Commande `stop` → `tts.cancel()` + `_setIdle()` (caméra non affectée) | ✅ |

### Phase 6 — Prompt DESCRIBE raccourci

| Fichier | Changement | Statut |
|---------|-----------|--------|
| `backend/api/describe.py` | Prompt réduit à 1 phrase < 20 mots (vue d'ensemble) | ✅ |

### Phase 7 — Retour haptique

| Fichier | Changement | Statut |
|---------|-----------|--------|
| `frontend/js/app.js` | `_setBusy()` → `navigator.vibrate?.(80)` ; `_setIdle()` → `navigator.vibrate?.([80, 60, 80])` | ✅ |

### Phase 8 — Désactivation des boutons pendant traitement

| Fichier | Changement | Statut |
|---------|-----------|--------|
| `frontend/js/app.js` | `_setBusy()` → `_actionBtns.forEach(b => b.disabled = true)` ; `_setIdle()` → `b.disabled = false` | ✅ |

### Phase 9 — Réorganisation des boutons

| Fichier | Changement | Statut |
|---------|-----------|--------|
| `frontend/index.html` | DESCRIBE pleine largeur, TEXT + DETAILS + ASK sur même ligne | ✅ |
| `frontend/css/style.css` | TEXT, DETAILS, ASK à `height: 80px` identiques | ✅ |

---

## Tableau de vérification

| Test | Attendu | Statut |
|------|---------|--------|
| Ouverture de l'app | Caméra démarre, TTS "A-Eyes ready..." | À tester |
| Permission caméra refusée | TTS "Camera unavailable. Please check permissions." | À tester |
| Clic bouton DESCRIBE | TTS "Analysing scene..." → 1 phrase globale | À tester |
| Clic bouton TEXT (texte visible) | TTS "Reading text..." → texte dicté | À tester |
| Clic bouton TEXT (pas de texte) | TTS "No text detected in the image." | À tester |
| Clic bouton DETAILS après DESCRIBE | TTS "Analysing in detail..." → 2-3 phrases | À tester |
| Clic bouton DETAILS sans capture | TTS "Please describe or read text first." | À tester |
| Clic bouton ASK | TTS "Speak your question." → attente voix → réponse | À tester |
| Commande vocale pendant TTS ou API | Ignorée (micro arrêté — `stopListening`) | À tester |
| Commande vocale "stop" pendant traitement | Lecture et traitement interrompus, caméra active | À tester |
| Commande vocale "help" | TTS "Available commands: describe, text, details, ask, repeat, stop." | À tester |
| Bouton REPEAT | Relit le dernier message | À tester |
| Vibration au déclenchement (DESCRIBE/TEXT/etc.) | Vibration courte 80 ms | À tester |
| Vibration à la fin du traitement | Double vibration 80-60-80 ms | À tester |
| Boutons désactivés pendant traitement | Clic sur bouton pendant analyse → ignoré | À tester |
| `POST /api/details` via Swagger `/docs` | JSON `{"text": "..."}` retourné | À tester |

---

## Problèmes connus

| ID | Description | Priorité |
|----|-------------|----------|
| P-01 | Sur Firefox, Web Speech API non supportée — boutons fonctionnels mais commandes vocales désactivées | Faible |
| P-02 | Si la clé OpenAI est épuisée ou invalide, les endpoints retournent un message d'erreur vocal | Documenté |

> Les problèmes rencontrés et leurs solutions détaillées sont documentés dans `Docs/V3/problemes_solutions_V3.md`.

---

## Feuille de route V4 (à planifier)

- PWA (Progressive Web App) : installation sur l'écran d'accueil mobile, mode hors-ligne partiel.
- Internationalisation : détection de langue du texte OCR, adaptation de la voix TTS.
- Historique vocal : navigation dans les dernières descriptions dictées.

