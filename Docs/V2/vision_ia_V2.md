# A-Eyes — V2 : Branchement IA de vision

> Projet étudiant / POC — La V1 a posé l'infrastructure (SPA + FastAPI + déploiement Render). L'endpoint `POST /api/describe` retourne encore un stub. L'objectif de la V2 est de brancher un modèle de vision réel sur cet endpoint pour que l'application décrive effectivement la scène capturée à l'utilisateur malvoyant.

---

## 1. Ce que la V1 a préparé

L'endpoint `POST /api/describe` dans `backend/api/describe.py` est conçu pour recevoir un frame JPEG depuis le navigateur et retourner un JSON `{"text": "..."}` lu ensuite par le TTS. En V1, il renvoie un message fixe (stub). La V2 consiste uniquement à remplacer ce stub par un appel réel à un modèle de vision multimodal.

Le `render.yaml` prévoit déjà un slot `OPENAI_API_KEY` commenté, prêt à être activé.

---

## 2. Étude de marché — modèles de vision disponibles par API

Les critères d'évaluation retenus pour A-Eyes sont : qualité de description de scène, qualité du français, latence (objectif < 1 s), coût/tier gratuit, conformité RGPD (localisation des données), et complexité d'intégration.

---

### 2.1 OpenAI — GPT-4o · GPT-4o mini · GPT-4.1 mini

Acteur de référence du marché. La famille GPT-4o accepte des images en base64 ou par URL via l'API `chat.completions`.

| Critère | GPT-4o | GPT-4o mini | GPT-4.1 mini |
|---------|--------|-------------|--------------|
| Qualité vision | Excellente | Très bonne | Très bonne |
| Qualité français | Excellente | Très bonne | Très bonne |
| Latence typique | 1,5–3 s | 0,5–1,5 s | 0,4–1,2 s |
| Tarif input ($/M tokens) | ~2,50 | ~0,15 | ~0,10 |
| Tier gratuit | Crédit 5 $ à l'inscription | idem | idem |
| CB requise | Non (crédit initial) | idem | idem |
| Localisation données | USA (OpenAI) | idem | idem |
| SDK Python | `openai` — très mature | idem | idem |

Avantage principal : documentation exhaustive, SDK le plus utilisé du marché, déjà référencé dans le code de la V1.
Limite : crédit initial non renouvelable ; après 5 $, facturation obligatoire.

---

### 2.2 Google — Gemini 2.0 Flash · Gemini 1.5 Flash · Gemini 1.5 Pro

Google propose un tier gratuit permanent via Google AI Studio, sans carte bancaire, ce qui en fait l'option la plus accessible pour un POC étudiant.

| Critère | Gemini 2.0 Flash | Gemini 1.5 Flash | Gemini 1.5 Pro |
|---------|-----------------|-----------------|----------------|
| Qualité vision | Très bonne | Très bonne | Excellente |
| Qualité français | Très bonne | Bonne | Très bonne |
| Latence typique | 0,3–0,8 s | 0,5–1,5 s | 1–3 s |
| Tarif input ($/M tokens) | Gratuit (quota) puis ~0,10 | Gratuit (quota) puis ~0,075 | ~1,25 |
| Tier gratuit permanent | Oui — 15 req/min | Oui — 15 req/min | Oui — 2 req/min |
| CB requise | Non | Non | Non |
| Localisation données | USA / UE selon région | idem | idem |
| SDK Python | `google-generativeai` | idem | idem |

Avantage principal : seul acteur majeur avec un tier gratuit permanent sans CB ; Gemini 2.0 Flash est le modèle le plus rapide du panel.
Limite : les données transitent par les serveurs Google (USA par défaut) ; la région européenne est disponible mais non garantie sur le tier gratuit.

---

### 2.3 Anthropic — Claude 3.7 Sonnet · Claude 3.5 Haiku

Anthropic se distingue par la qualité rédactionnelle de ses descriptions — les sorties sont naturellement bien structurées pour une lecture TTS.

| Critère | Claude 3.7 Sonnet | Claude 3.5 Haiku |
|---------|------------------|-----------------|
| Qualité vision | Excellente | Très bonne |
| Qualité français | Excellente | Très bonne |
| Latence typique | 1,5–3 s | 0,5–1,5 s |
| Tarif input ($/M tokens) | ~3,00 | ~0,80 |
| Tier gratuit | Crédit initial uniquement | idem |
| CB requise | Non (crédit initial) | idem |
| Localisation données | USA (AWS us-east-1) | idem |
| SDK Python | `anthropic` | idem |

Avantage principal : qualité rédactionnelle supérieure pour les descriptions destinées au TTS.
Limite : pas de tier gratuit permanent ; le tarif de Haiku reste plus élevé que GPT-4o mini.

---

### 2.4 Meta — Llama 3.2 Vision 11B / 90B (via Groq, Together AI, Fireworks AI)

Llama 3.2 Vision est un modèle open-source que l'on peut consommer via des API d'inférence hébergées. Groq offre un accès gratuit avec un quota quotidien.

| Critère | Llama 3.2 Vision 11B (Groq) | Llama 3.2 Vision 90B |
|---------|-----------------------------|----------------------|
| Qualité vision | Bonne | Très bonne |
| Qualité français | Correcte | Bonne |
| Latence typique | < 0,5 s (inférence Groq LPU) | 1–2 s |
| Tarif | Gratuit (quota quotidien) | ~0,90 $/M tokens (Together AI) |
| Tier gratuit permanent | Oui (Groq) | Non |
| CB requise | Non (Groq) | Oui |
| Localisation données | USA (Groq) | USA |
| SDK Python | `groq` ou `openai` (compatible) | idem |

Avantage principal : latence extrêmement faible sur Groq grâce aux LPU ; tier gratuit sans CB.
Limite : qualité des descriptions en français inférieure aux modèles propriétaires ; quota quotidien limité sur Groq.

---

### 2.5 Mistral AI — Pixtral 12B · Pixtral Large

Mistral est un acteur européen (Paris), ce qui est un avantage direct pour la conformité RGPD : les données peuvent être traitées sur infrastructure européenne.

| Critère | Pixtral 12B | Pixtral Large |
|---------|-------------|---------------|
| Qualité vision | Bonne | Très bonne |
| Qualité français | Très bonne (modèle français) | Excellente |
| Latence typique | 0,8–2 s | 1,5–3 s |
| Tarif input ($/M tokens) | ~0,15 | ~2,00 |
| Tier gratuit | Crédit initial (La Plateforme) | idem |
| CB requise | Non (crédit initial) | idem |
| Localisation données | UE (France) | idem |
| SDK Python | `mistralai` (compatible OpenAI) | idem |

Avantage principal : acteur européen, données hébergées en France — avantage RGPD fort. Très bonne qualité en français (modèle entraîné sur corpus francophone dense).
Limite : pas de tier gratuit permanent ; Pixtral Large est coûteux.

---

### 2.6 xAI — Grok Vision (Grok-2 Vision)

Proposé par xAI (Elon Musk), Grok-2 Vision est accessible via API depuis fin 2024.

| Critère | Grok-2 Vision |
|---------|---------------|
| Qualité vision | Très bonne |
| Qualité français | Bonne |
| Latence typique | 1–2,5 s |
| Tarif input ($/M tokens) | ~2,00 |
| Tier gratuit | Oui (quota mensuel via xAI console) |
| CB requise | Non (quota initial) |
| Localisation données | USA |
| SDK Python | Compatible API OpenAI |

Avantage principal : quota mensuel gratuit, compatible SDK OpenAI (migration sans réécriture).
Limite : écosystème moins mature, documentation moins fournie, qualité français correcte mais pas optimale.

---

### 2.7 Amazon — Nova Pro / Nova Lite (via AWS Bedrock)

AWS Bedrock expose les modèles Amazon Nova avec vision. Pertinent en contexte entreprise, mais inadapté à un POC étudiant.

| Critère | Amazon Nova Pro | Amazon Nova Lite |
|---------|----------------|-----------------|
| Qualité vision | Très bonne | Bonne |
| Qualité français | Bonne | Correcte |
| Latence typique | 1–3 s | 0,5–1,5 s |
| Tarif input ($/M tokens) | ~0,80 | ~0,06 |
| Tier gratuit | AWS Free Tier 12 mois (limité) | idem |
| CB requise | Oui | Oui |
| Localisation données | Région AWS au choix (UE disponible) | idem |
| SDK Python | `boto3` — verbeux | idem |

Avantage principal : tarif Nova Lite très compétitif ; données hébergées en UE possible.
Limite : CB obligatoire, `boto3` verbeux, complexité IAM/VPC — surdimensionné pour un POC.

---

### 2.8 Microsoft Azure — Azure OpenAI Vision + Azure AI Vision

Azure expose les modèles OpenAI (GPT-4o) via sa propre infrastructure, avec hébergement UE disponible. Azure AI Vision est un service dédié à l'analyse d'images (plus limité que les LLM multimodaux).

| Critère | Azure OpenAI (GPT-4o) | Azure AI Vision |
|---------|-----------------------|-----------------|
| Qualité vision | Excellente (même modèle qu'OpenAI) | Bonne (classification, OCR, description basique) |
| Qualité français | Excellente | Correcte |
| Latence typique | 1,5–3 s | 0,3–0,8 s |
| Tier gratuit | Non | Oui (5 000 transactions/mois) |
| CB requise | Oui | Oui |
| Localisation données | UE (West Europe) possible | idem |
| SDK Python | `openai` (même SDK) | `azure-ai-vision-imageanalysis` |

Avantage principal : données en UE garanties, RGPD fort, même qualité que OpenAI direct.
Limite : CB obligatoire, déploiement Azure complexe pour un POC — pertinent en contexte entreprise/production.

---

### 2.9 Tableau récapitulatif

| Acteur / Modèle | Qualité vision FR | Latence | Tier gratuit permanent | CB requise | RGPD (données UE) | Complexité intégration |
|---|---|---|---|---|---|---|
| OpenAI GPT-4o | Excellente | Moyenne | Non (crédit 5$) | Non | Non (USA) | Très faible |
| OpenAI GPT-4o mini | Très bonne | Faible | Non (crédit 5$) | Non | Non (USA) | Très faible |
| OpenAI GPT-4.1 mini | Très bonne | Faible | Non (crédit 5$) | Non | Non (USA) | Très faible |
| Google Gemini 2.0 Flash | Très bonne | Très faible | Oui (15 req/min) | Non | Partiel | Faible |
| Google Gemini 1.5 Flash | Très bonne | Faible | Oui (15 req/min) | Non | Partiel | Faible |
| Anthropic Claude 3.5 Haiku | Très bonne | Faible | Non (crédit initial) | Non | Non (USA) | Faible |
| Anthropic Claude 3.7 Sonnet | Excellente | Moyenne | Non (crédit initial) | Non | Non (USA) | Faible |
| Meta Llama 3.2 11B (Groq) | Correcte | Très faible | Oui (quota/jour) | Non | Non (USA) | Faible |
| Mistral Pixtral 12B | Bonne (FR natif) | Faible | Non (crédit initial) | Non | Oui (France) | Faible |
| Mistral Pixtral Large | Excellente (FR natif) | Moyenne | Non (crédit initial) | Non | Oui (France) | Faible |
| xAI Grok-2 Vision | Bonne | Moyenne | Oui (quota mensuel) | Non | Non (USA) | Très faible |
| Amazon Nova Lite | Correcte | Faible | Non (CB requise) | Oui | Possible (UE) | Élevée |
| Azure OpenAI GPT-4o | Excellente | Moyenne | Non | Oui | Oui (UE) | Moyenne |

---

## 3. Recommandation pour le POC

### Critères de sélection

Pour un POC étudiant sur A-Eyes, trois contraintes sont non-négociables :

1. Budget zéro — aucune facturation tant que le POC est en cours de validation
2. Qualité français — les descriptions sont lues par TTS à des utilisateurs francophones malvoyants ; une description approximative dégrade directement l'expérience
3. Latence — l'objectif projet est < 1 s (PDF p.6)

### Modèle retenu : GPT-4o mini (OpenAI)

GPT-4o mini est le choix retenu pour la V2 pour les raisons suivantes :

- Déjà référencé dans le code — `describe.py` et `render.yaml` pointent vers l'écosystème OpenAI. La migration du stub vers l'appel réel se fait en moins de 10 lignes, sans changer de SDK ni de configuration.
- Crédit de démarrage sans CB — 5 $ offerts à l'inscription couvrent ~500 analyses (à ~0,01 $/image), largement suffisant pour un POC.
- Qualité/latence équilibrées — très bonne compréhension de scène, descriptions naturelles en français, latence < 1 s dans la majorité des cas.
- SDK le plus documenté — `openai` Python est la référence du marché ; les exemples, les traitements d'erreurs et les patterns async sont les mieux couverts.

### Alternative sérieuse : Gemini 2.0 Flash (Google)

Si le crédit OpenAI est épuisé ou si le POC dure plusieurs mois, Gemini 2.0 Flash est l'alternative la plus crédible : tier gratuit permanent (15 req/min), latence inférieure, et qualité suffisante pour le cas d'usage. La migration depuis OpenAI vers Gemini représente ~20 lignes de code dans `describe.py`.

### Note RGPD pour une version production

Si le projet sort du cadre POC pour devenir une application accessible au public, Mistral Pixtral (données hébergées en France) ou Azure OpenAI avec région West Europe seraient à privilégier pour garantir la conformité RGPD sans dépendre d'un hébergement américain.

---

## 4. Modifications à apporter en V2

La surface de code à modifier est minimale — c'est l'un des acquis de la V1.

### 4.1 `backend/requirements.txt`

Ajouter la dépendance :

```
openai>=1.0.0
```

### 4.2 `backend/api/describe.py`

Remplacer le stub par l'appel GPT-4o (code déjà fourni en commentaire dans le fichier).

### 4.3 `render.yaml`

Décommenter et renseigner la variable d'environnement :

```yaml
envVars:
  - key: OPENAI_API_KEY
    sync: false   # valeur saisie manuellement dans le dashboard Render
```

### 4.4 Prompt

Le prompt envoyé avec l'image conditionne directement la qualité du TTS. Piste retenue :

```
Décris cette scène en deux phrases maximum pour une personne malvoyante.
Sois précis sur les objets, les personnes et les actions visibles.
N'utilise pas de formule d'introduction comme "Je vois" ou "Sur cette image".
```

---

## 5. Points de vigilance

- RGPD — en V1, les frames ne quittaient pas le navigateur (stub). En V2, chaque frame est envoyée à OpenAI. Il faut informer l'utilisateur et s'assurer qu'aucun stockage côté serveur A-Eyes n'est effectué (`describe.py` ne doit pas écrire le fichier sur disque).
- Temps de réponse — la contrainte projet est < 1 s (PDF p.6). GPT-4o mini atteint cet objectif dans la majorité des cas ; GPT-4o peut dépasser 1 s selon la charge réseau. À mesurer en V2.
- Gestion des erreurs — en cas d'échec de l'appel API (quota dépassé, timeout), `describe.py` doit retourner un message d'erreur lisible par le TTS plutôt qu'une exception HTTP brute.
