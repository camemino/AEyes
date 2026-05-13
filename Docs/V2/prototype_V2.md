# A-Eyes — Prototype V2 : Branchement IA (ChatGPT)

> **Périmètre V2** : remplacement du stub `POST /api/describe` par un appel réel à l'API OpenAI (`gpt-4.1-mini`).  
> **Date** : 13/05/2026  
> **Base** : V1 (SPA + FastAPI + déploiement Render)

---

## Ce qui a changé fonctionnellement

### Avant (V1 stub)

Lorsque l'utilisateur appuyait sur le bouton "Scan", l'application retournait toujours le même message fixe :
> *"Analysis in progress... feature available in version 1."*

Aucune image n'était analysée. Le TTS lisait ce texte statique à chaque fois.

### Maintenant (V2)

Le bouton "Scan" capture un frame réel depuis la caméra, l'envoie au backend, et reçoit une description générée par `gpt-4.1-mini` basée sur ce que la caméra voit réellement.

Exemples de descriptions retournées :

- *"A person is sitting at a desk in front of a laptop. There is a cup of coffee on the right side. The room appears to be a home office with natural light coming from the left."*
- *"The image shows a street intersection with pedestrians crossing. A red traffic light is visible in the upper right corner."*

Le TTS lit cette description à voix haute immédiatement après réception.

---

## Ce qui a changé par rapport à la V1

### Backend

| Fichier | Modification |
|---------|-------------|
| `backend/api/describe.py` | Stub supprimé — appel `gpt-4.1-mini` via `openai.AsyncOpenAI` avec prompt système orienté TTS |
| `backend/config.py` | Lecture de `OPENAI_API_KEY` depuis l'environnement via `os.getenv` + chargement automatique de `backend/.env` en local (`python-dotenv`) |
| `backend/requirements.txt` | Ajout de `openai>=1.0.0` et `python-dotenv>=1.0.0` |
| `render.yaml` | Slot `OPENAI_API_KEY` activé avec `sync: false` (valeur saisie manuellement dans le dashboard Render) |

### Modèle retenu

`gpt-4.1-mini` — choisi pour son rapport latence/coût optimal (0,4–1,2 s · $0,10/M tokens) parmi les modèles OpenAI étudiés dans [vision_ia_V2.md](vision_ia_V2.md).

### Prompt système

```
You are a visual description assistant for visually impaired people.
Describe this scene in English in 2 to 3 short sentences,
suitable for text-to-speech reading.
```

### Gestion d'erreur

En cas d'échec de l'appel OpenAI (`openai.OpenAIError`), l'endpoint retourne :
```json
{"text": "Unable to analyze the image at the moment."}
```
avec un code HTTP `502` et un log serveur.

---

## Infrastructure & secrets

| Où | Variable | Rôle |
|----|----------|------|
| Render dashboard › Environment | `OPENAI_API_KEY` | Lue par le code Python en production |
| `backend/.env` (local, non commité) | `OPENAI_API_KEY` | Développement local uniquement |

Le redéploiement sur Render est déclenché automatiquement à chaque push sur `main` (Auto-Deploy natif Render — aucun workflow CI/CD externe requis).

---

## Ce qui n'a pas changé

- L'interface frontend (HTML/CSS/JS) est inchangée — elle consomme déjà `POST /api/describe` et lit le champ `text` pour le TTS.
- La structure du JSON de réponse (`{"text": "..."}`) est identique.
- Le déploiement Render reste sur le plan gratuit (région Frankfurt).

---

## Limites connues du prototype

| Limite | Impact |
|--------|--------|
| Crédit OpenAI non renouvelable (5 $ à l'inscription) | Après épuisement, facturation obligatoire |
| Latence réseau + inférence ~0,4–1,2 s | L'objectif < 1 s peut ne pas être tenu selon la charge |
| Données image transmises aux serveurs OpenAI (USA) | Point RGPD à surveiller pour une mise en production réelle |
| Plan Render gratuit — mise en veille après 15 min | Premier appel après veille peut dépasser 30 s |
