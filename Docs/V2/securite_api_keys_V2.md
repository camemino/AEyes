# Gestion des clés API dans une application web — Problématique & solutions

> Document de référence pour le projet A-Eyes — applicable à tout projet web exposant une clé API tierce.

---

## 1. La problématique

Une clé API (comme `OPENAI_API_KEY`) est une **credential secrète** : quiconque la possède peut effectuer des appels à l'API en ton nom, consommer ton quota et générer des coûts.

Dans une application web, deux surfaces d'exposition existent :

### Côté frontend (navigateur)

Tout ce qui est dans le code JavaScript — fichiers `.js`, variables d'environnement injectées au build (`VITE_`, `REACT_APP_`), `localStorage`, `sessionStorage` — est **lisible par n'importe qui** via les DevTools du navigateur ou en inspectant les sources de la page.

> Règle absolue : une clé API ne doit jamais se trouver dans le code frontend.

### Côté backend (serveur)

Le code serveur n'est pas accessible depuis le navigateur. C'est le seul endroit où une clé API peut être utilisée en sécurité.

---

## 2. Les solutions

### 2.1 Variable d'environnement sur le serveur ✅ Recommandé

La clé est injectée dans le processus serveur via une variable d'environnement (`os.getenv`). Elle n'apparaît jamais dans le code source ni dans le dépôt Git.

| Avantage | Inconvénient |
|----------|-------------|
| Simple, universelle, support natif sur tous les PaaS | Nécessite un accès au serveur / dashboard pour la modifier |
| Zéro code spécifique | Risque de fuite dans les logs si on affiche accidentellement les variables d'env |
| Standard industrie (12-Factor App) | |

### 2.2 Fichier `.env` local (développement uniquement)

Un fichier `.env` non commité contient les clés pour le développement local. La bibliothèque `python-dotenv` le charge au démarrage. Le fichier est exclu de Git via `.gitignore`.

| Avantage | Inconvénient |
|----------|-------------|
| Pratique en local, pas de manipulation de variables système | Ne doit jamais être commité (risque humain) |
| Compatible avec les variables d'env de production | Doit être recréé manuellement sur chaque poste développeur |

### 2.3 Secret Manager (ex: AWS Secrets Manager, Azure Key Vault, HashiCorp Vault)

Les clés sont stockées dans un service dédié au chiffrement et à la rotation des secrets. Le code les récupère à l'exécution via une API sécurisée.

| Avantage | Inconvénient |
|----------|-------------|
| Rotation automatique des clés | Complexité d'intégration élevée |
| Audit trail complet | Coût supplémentaire |
| Idéal pour les environnements de production critiques | Surdimensionné pour un POC étudiant |

### 2.4 Secrets CI/CD (ex: GitHub Secrets, GitLab CI Variables)

Les clés sont stockées dans le système de CI/CD et injectées uniquement pendant le pipeline (build, tests, déploiement). Elles ne transitent jamais dans le dépôt.

| Avantage | Inconvénient |
|----------|-------------|
| Chiffrées et masquées dans les logs CI | Disponibles uniquement pendant le pipeline, pas en runtime |
| Intégration native GitHub/GitLab | Ne remplace pas les variables d'env de production |

### 2.5 Ce qu'il ne faut jamais faire ❌

| Pratique interdite | Risque |
|--------------------|--------|
| Écrire la clé en dur dans le code (`api_key = "sk-..."`) | Exposée dans Git, visible par tous les contributeurs et dans l'historique |
| La stocker dans le `localStorage` / `sessionStorage` | Accessible depuis n'importe quel script JS de la page (XSS) |
| La transmettre via une URL (`?api_key=sk-...`) | Visible dans les logs serveur, l'historique navigateur, les proxies |
| La commiter dans `.env` | Permanente dans l'historique Git même après suppression |

---

## 3. Solution retenue pour A-Eyes (POC)

A-Eyes suit l'architecture **BFF (Backend For Frontend)** : le frontend ne connaît pas la clé OpenAI et ne l'utilise jamais directement. Seul le backend FastAPI effectue les appels à l'API OpenAI.

```
Navigateur
  │
  │  POST /api/describe  (frame JPEG)
  ▼
Backend FastAPI          ← OPENAI_API_KEY chargée depuis l'environnement
  │
  │  POST api.openai.com/v1/chat/completions
  ▼
OpenAI GPT-4.1-mini
```

### En développement local

- La clé est dans `backend/.env` (ignoré par `.gitignore`)
- `python-dotenv` la charge automatiquement au démarrage via `load_dotenv()` dans `config.py`

### En production (Render)

- La clé est saisie manuellement dans Render › dashboard › Environment Variables
- Elle est chiffrée au repos et masquée dans l'interface
- Elle est injectée comme variable d'environnement dans le processus Python au démarrage du service
- `render.yaml` déclare le slot avec `sync: false` (valeur jamais stockée dans le dépôt Git)

### Ce qui n'est jamais dans Git

- La valeur réelle de `OPENAI_API_KEY`
- Le fichier `backend/.env`
