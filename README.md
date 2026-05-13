# A-Eyes

Application d'assistance visuelle — caméra web → description IA → synthèse vocale.

## Architecture

```
backend/   FastAPI — sert l'API ET les fichiers statiques du frontend
frontend/  SPA HTML/CSS/JS — caméra + TTS + commandes vocales
Src/       Application Kivy (version bureau, indépendante)
```

## Déploiement rapide sur Render (plan gratuit)

1. Pushez ce dépôt sur GitHub.
2. Sur [render.com](https://render.com) → **New** → **Blueprint**.
3. Connectez votre repo GitHub — Render détecte automatiquement le fichier `render.yaml`.
4. Cliquez **Apply** — le service `a-eyes` sera créé et déployé.
5. Dans le dashboard Render → votre service → **Environment**, ajoutez la variable :
   - `OPENAI_API_KEY` = votre clé OpenAI (`sk-...`)
6. Une fois le build terminé, accédez à l'URL fournie par Render.

> **Auto-Deploy** : Render redéploie automatiquement le service à chaque push sur `main`.

> **Note** : sur le plan gratuit, le service se met en veille après 15 min d'inactivité  
> et redémarre (~30 s) à la prochaine requête.

## Développement local

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload
```

Ouvrez <http://localhost:8000>.

## Variables d'environnement

| Variable | Description | Requis |
|----------|-------------|--------|
| `OPENAI_API_KEY` | Clé API OpenAI — modèle `gpt-4.1-mini` pour la description de scène | Oui (V1) |

Pour le développement local, créez un fichier `.env` à la racine du dossier `backend/` :

```
OPENAI_API_KEY=sk-...
```

> Ne commitez jamais ce fichier — il est ignoré par `.gitignore`.
