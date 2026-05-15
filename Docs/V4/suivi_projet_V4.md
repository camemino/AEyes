# Suivi de projet V4 — A-Eyes

## Contexte

V4 : ajout du mode FIND — recherche guidée d'un objet par la voix, avec instructions directionnelles vocales ("Turn right", "Straight ahead"…) et bips mono (onde carrée). Suppression de l'affichage caméra. Adapté à une démo sur téléphone simple (pas de haut-parleur stéréo requis).

---

## Phases d'implémentation

### Phase 1 — Backend : endpoint `/api/find` et `FIND_PROMPT`

| Fichier | Changement | Statut |
|---------|-----------|--------|
| `backend/prompts.py` | Ajout `FIND_PROMPT` (sortie JSON stricte, instructions directionnelles, champ `direction`, ≤ 5 mots) | ✅ |
| `backend/api/find.py` | Nouveau endpoint `POST /api/find` (`detail: "low"`, `response_format=json_object`, sanitisation `direction`, fallback `not_visible`) | ✅ |
| `backend/main.py` | Import `find_router` + `app.include_router(find_router, prefix="/api")` | ✅ |

### Phase 2 — Frontend audio : `Beeper` (3 sons mono, onde carrée)

| Fichier | Changement | Statut |
|---------|-----------|--------|
| `frontend/js/find.js` (nouveau) | Classe `Beeper` : `init()`, `resume()`, `beepFound()` (880 Hz 120 ms + 1320 Hz 180 ms), `beepLost()` (300→220 Hz 250 ms), `beepScan()` (520 Hz 80 ms) — oscillateur `square` | ✅ |

### Phase 3 — Frontend logique : `FindSession`

| Fichier | Changement | Statut |
|---------|-----------|--------|
| `frontend/js/find.js` | Classe `FindSession` : boucle chaînée sur TTS, `_lastSpoken` pour déduplication, `beepScan()` avant chaque appel API, downscale 512 px JPEG 0.7, timeout 30 s, `cancel()` | ✅ |
| `frontend/js/find.js` | Fonction `_downscale(dataURL)` : canvas resize + `toBlob` JPEG 0.7 | ✅ |

### Phase 4 — Commande vocale `find <target>`

| Fichier | Changement | Statut |
|---------|-----------|--------|
| `frontend/js/voice.js` | Ajout `find: 'find'` dans la table `COMMANDS` | ✅ |
| `frontend/js/voice.js` | Parsing `"find <target>"` (calqué sur `"ask <question>"`) → `_onCommand('find:' + target)` | ✅ |

### Phase 5 — Intégration dans `app.js`

| Fichier | Changement | Statut |
|---------|-----------|--------|
| `frontend/js/app.js` | Import `Beeper` et `FindSession` depuis `find.js` | ✅ |
| `frontend/js/app.js` | Ajout `this._beeper = new Beeper()` | ✅ |
| `frontend/js/app.js` | Ajout `this._findSession = null` | ✅ |
| `frontend/js/app.js` | Init `AudioContext` au premier `pointerdown` (iOS Safari) | ✅ |
| `frontend/js/app.js` | Câblage `#btn-find-stop` → `this._findSession?.cancel()` | ✅ |
| `frontend/js/app.js` | Branche `find:` dans `_handleCommand` | ✅ |
| `frontend/js/app.js` | Isolation commandes pendant session FIND (seul "stop" passe) | ✅ |
| `frontend/js/app.js` | Nouvelle méthode `onFind(target)` | ✅ |

### Phase 6 — UI : overlay STOP

| Fichier | Changement | Statut |
|---------|-----------|--------|
| `frontend/index.html` | Overlay `#find-overlay` (masqué par défaut) + `<p>` + `<button id="btn-find-stop">` | ✅ |
| `frontend/css/style.css` | Styles overlay : `position: fixed; inset: 0`, fond noir 85 %, flex centré | ✅ |
| `frontend/css/style.css` | Styles `.btn-stop` : rouge, 80 % largeur, 140 px hauteur, texte 48 px | ✅ |

### Phase 7 — Correction bug CSS préexistant

| Fichier | Changement | Statut |
|---------|-----------|--------|
| `frontend/css/style.css` | Ajout du sélecteur `.btn-repeat {` manquant (propriétés orphelines) | ✅ |

### Phase 8 — Suppression de l'affichage caméra

| Fichier | Changement | Statut |
|---------|-----------|--------|
| `frontend/index.html` | Suppression `#camera-container` + placeholder ; `<video>` rendue invisible (1×1 px, opacity 0) | ✅ |
| `frontend/css/style.css` | Suppression des blocs `#camera-container`, `#camera-placeholder`, `#camera-view` | ✅ |
| `frontend/js/app.js` | Suppression de `_placeholder`, simplification `_startCamera()` et `_stopCamera()` | ✅ |

---

## Tableau de vérification

| Test | Attendu | Statut |
|------|---------|--------|
| `curl -F "file=@img.jpg" -F "target=phone" /api/find` | JSON `{direction, distance, text, confidence}`, `direction` dans l'énum | À tester |
| Démarrage app | Comportement V3 inchangé | À tester |
| Dire "find my phone" (objet visible, centré) | TTS "Looking for my phone." → double bip + "Found it!" | À tester |
| Dire "find my keys" (objet à droite) | TTS "Turn right" en approchant → guidage jusqu'à "Found it!" | À tester |
| Guidage sans changement de direction | Silence entre itérations (pas de répétition de la même phrase) | À tester |
| Dire "stop" pendant session | Overlay disparaît, TTS "Search cancelled.", boutons réactivés | À tester |
| Clic sur bouton STOP (overlay) | Idem | À tester |
| Timeout 30 s (objet non trouvé) | TTS "I cannot find it.", session fermée | À tester |
| Clic sur DESCRIBE pendant session FIND | Ignoré (commande bloquée pendant session) | À tester |
| iOS Safari — bips après premier tap | Double bip audible sur iPhone | À tester |
| iOS Safari — bips sans tap préalable | Bips silencieux mais guidage vocal OK | À tester |
| Affichage écran — boutons plein écran | Caméra invisible, boutons occupent toute la hauteur | À tester |
| Bip scan audible à chaque photo | Son court neutre (520 Hz) entendu avant chaque guidage | À tester |
| Network DevTools `/api/find` | Temps de réponse < 1.5 s | À tester |
| Tokens par appel (logs OpenAI) | ≤ 400 tokens total | À tester |
| Bouton REPEAT fonctionne | Style appliqué, comportement inchangé (bug CSS corrigé) | À tester |

---

## Problèmes connus

| ID | Description | Priorité |
|----|-------------|----------|
| P-01 | Sur Firefox, Web Speech API non supportée — commande "find" non disponible (boutons OK) | Faible |
| P-02 | En environnement très bruyant, la reconnaissance de "find \<objet\>" peut être imprécise | Faible |
| P-03 | Sans tap préalable sur iOS Safari, les bips sont silencieux (politique Apple AudioContext) | Documenté |

---
