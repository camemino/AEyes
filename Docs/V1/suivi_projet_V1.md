# A-Eyes — Suivi de projet V1

> **Périmètre V1** : migration de l'application Kivy (desktop/Android) vers une application web (SPA + backend FastAPI).
> **Date de début** : 19/04/2026
> **Responsable** : équipe A-Eyes

---

## Statut global

| Phase | Statut | Date |
|---|---|---|
| 1 — Planification & architecture | ✅ Terminé | 19/04/2026 |
| 2 — Backend FastAPI | ✅ Terminé | 19/04/2026 |
| 3 — Frontend HTML/CSS | ✅ Terminé | 19/04/2026 |
| 4 — Modules JS (caméra, TTS, voix) | ✅ Terminé | 19/04/2026 |
| 5 — Intégration & tests manuels | 🔄 En cours | 19/04/2026 |
| 6 — Correctifs & polish UI | 🔄 En cours | 19/04/2026 |
| 7 — Préparation repo GitHub & déploiement Render | ✅ Terminé | 19/04/2026 |
| 8 — Déploiement / PWA | ⬜ À faire | — |

---

## Journal des étapes

### ✅ Phase 1 — Planification & architecture (19/04/2026)

**Objectif :** définir la stack technique et le plan de migration avant toute ligne de code.

**Réalisé :**
- Analyse du code Kivy existant (`main.py`, `config.py`, `a_eyes.kv`, `capture.py`, `speaker.py`, `listener.py`)
- Identification des équivalents navigateur pour chaque dépendance système :
  - `cv2.VideoCapture` → `MediaDevices.getUserMedia()`
  - `win32com` SAPI → `SpeechSynthesis` API
  - `speech_recognition` + `pyaudio` → `SpeechRecognition` API
- Choix de FastAPI comme backend (léger, async, génération automatique de doc OpenAPI)
- Décision SPA (Single Page Application) sans framework JS pour limiter les dépendances
- Création de [architecture_V1.md](architecture_V1.md)

---

### ✅ Phase 2 — Backend FastAPI (19/04/2026)

**Objectif :** créer le serveur Python qui sert le frontend et expose l'API.

**Fichiers créés :**
- `backend/main.py` — point d'entrée FastAPI, monte les fichiers statiques du frontend
- `backend/config.py` — constantes portées depuis `Src/config.py`
- `backend/requirements.txt` — `fastapi`, `uvicorn[standard]`, `python-multipart`
- `backend/api/__init__.py`
- `backend/api/describe.py` — `POST /api/describe` (stub V1, prêt pour branchement IA en V2)

**Décisions techniques :**
- CORS `allow_origins=["*"]` en développement (à restreindre en production)
- Le frontend est servi en statique par FastAPI (`StaticFiles`) : un seul processus suffit
- `describe.py` retourne le stub sans lire le fichier uploadé : aucune donnée utilisateur n'est traitée (RGPD V1)

**Commande de lancement :**
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

---

### ✅ Phase 3 — Frontend HTML/CSS (19/04/2026)

**Objectif :** créer l'interface visuelle haute accessibilité, fidèle aux couleurs et tailles de la V0.

**Fichiers créés :**
- `frontend/index.html` — SPA avec deux sections (`#main-screen` / `#settings-screen`)
- `frontend/css/style.css` — variables CSS calquées sur `config.py` (couleurs RGBA → hex, dp/sp → px)

**Points d'accessibilité implémentés :**
- `aria-label` sur tous les boutons et zones interactives
- `aria-pressed` sur le bouton SCAN (état on/off)
- `aria-live="polite"` sur l'affichage de la valeur du slider
- `focus-visible` avec contour jaune 4px (conforme WCAG 2.4.7)
- Responsive : variables CSS réduites sous 480 px (mobile portrait)

---

### ✅ Phase 4 — Modules JS (19/04/2026)

**Objectif :** implémenter les trois modules métier (caméra, TTS, voix) et le contrôleur principal.

**Fichiers créés :**

| Fichier | Remplace | API navigateur |
|---|---|---|
| `frontend/js/camera.js` | `camera/capture.py` | `MediaDevices.getUserMedia()` |
| `frontend/js/tts.js` | `tts/speaker.py` | `SpeechSynthesis` |
| `frontend/js/voice.js` | `voice_input/listener.py` | `SpeechRecognition` |
| `frontend/js/app.js` | `ui/main_screen.py` + `settings_screen.py` | — |

**Décisions techniques :**
- Modules ES natifs (`type="module"`) : pas de bundler, pas de build step
- `Camera.captureFrame()` utilise un `<canvas>` temporaire → Data URL JPEG envoyée au backend
- `Speaker.setRate(wpm)` : normalisation `wpm / 160` pour correspondre à l'échelle pyttsx3
- `VoiceListener` : auto-restart sur `onend` (le navigateur coupe la session après ~60s de silence)
- Table `COMMANDS` identique à `listener.py` : `scan`, `describe`, `repeat`, `settings`, `help`, `stop`

---

### 🔄 Phase 5 — Intégration & tests manuels (19/04/2026)

**Objectif :** valider le bon fonctionnement de l'application dans le navigateur.

**Tests effectués :**

| Fonctionnalité | Résultat | Notes |
|---|---|---|
| Serveur démarre (HTTP 200) | ✅ OK | `uvicorn` + venv projet |
| Page HTML chargée | ✅ OK | Titre "A-Eyes" vérifié |
| Navigation SETTINGS | ✅ OK (après correctif) | Voir Phase 6 |
| Navigation BACK | ✅ OK (après correctif) | Voir Phase 6 |
| Bouton SCAN | ⬜ À tester | Nécessite navigateur ouvert |
| Synthèse vocale TTS | ⬜ À tester | Chrome/Edge requis |
| Commandes vocales | ⬜ À tester | Chrome/Edge + micro requis |
| Bouton DESCRIBE | ⬜ À tester | Retourne stub V1 |
| Bouton REPEAT | ⬜ À tester | — |
| Slider vitesse TTS | ⬜ À tester | — |

---

### 🔄 Phase 6 — Correctifs & polish UI (19/04/2026)

**Correctif #1 — Écran Settings non affiché**

- **Symptôme :** l'écran `#settings-screen` restait visible même avec l'attribut `hidden`, les deux écrans s'affichaient simultanément.
- **Cause :** le sélecteur CSS `#settings-screen { display: flex }` a une spécificité qui écrase le comportement par défaut de `[hidden]`.
- **Correctif :** ajout de `[hidden] { display: none !important; }` dans `style.css`.
- **Fichier modifié :** `frontend/css/style.css`

---

### ✅ Phase 7 — Préparation repo GitHub & déploiement Render (19/04/2026)

**Objectif :** configurer le dépôt pour un déploiement automatique sur Render (plan gratuit).

**Fichiers créés :**

| Fichier | Rôle |
|---|---|
| `render.yaml` | Blueprint Render — déclare le service web, la commande de build et de démarrage |
| `.gitignore` | Exclut `.venv/`, `__pycache__/`, `.env`, `.vscode/` |
| `.env.example` | Modèle de variables d'environnement (sans secrets, versionné) |
| `README.md` | Instructions de déploiement Render et de développement local |

**Décisions techniques :**
- `rootDir: backend` dans `render.yaml` : Render exécute les commandes depuis `backend/`, aligné avec le `sys.path` de `main.py`
- `startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT` : Render injecte `$PORT` dynamiquement
- `plan: free` + `region: frankfurt` pour minimiser la latence Europe
- Un seul service suffit : FastAPI sert à la fois l'API (`/api/*`) et le frontend statique (`/`)

**Procédure de déploiement :**
1. `git push` vers GitHub
2. Render → **New → Blueprint** → connecter le repo
3. Render lit `render.yaml` et crée le service automatiquement

> **Limite plan gratuit :** veille après 15 min d'inactivité, redémarrage à froid ~30 s.

---

### ⬜ Phase 8 — Déploiement / PWA (à planifier)

**Objectif :** rendre l'application accessible hors `localhost` et installable sur mobile.

**Tâches prévues :**
- [ ] Ajouter `frontend/manifest.json` (icône, `display: standalone`, `theme_color`)
- [ ] Ajouter `frontend/js/sw.js` (service worker — cache des assets)
- [ ] Restreindre `allow_origins` dans `backend/main.py` au domaine Render de production
- [ ] Tester sur iOS Safari (SpeechSynthesis) et Android Chrome (SpeechRecognition)

---

## Problèmes connus

| # | Description | Priorité | Statut |
|---|---|---|---|
| P-01 | `SpeechRecognition` API non supportée sur Firefox | Basse | Documenté (navigateur incompatible) |
| P-02 | `getUserMedia` exige HTTPS hors `localhost` | Haute | Bloquant pour le déploiement — Phase 7 |
| P-03 | Backend ne valide pas le format du fichier uploadé sur `/api/describe` | Moyenne | À corriger en V2 |
