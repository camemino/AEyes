# Fonctionnalités V3 — A-Eyes

## Vue d'ensemble

La V3 porte sur l'amélioration de l'expérience utilisateur avec trois évolutions fonctionnelles :

1. Suppression du bouton SCAN — la caméra s'ouvre automatiquement.
2. Nouvelle feature **Text** — détecte et dicte le texte visible dans l'image.
3. Nouvelle feature **Details** — description détaillée de la dernière image capturée.
4. Suppression de l'écran Settings — simplification de l'interface.
5. Anti-boucle vocale — arrêt complet de la reconnaissance pendant tout traitement.
6. Retour haptique — vibration à chaque début et fin de traitement.
7. Désactivation des boutons d'action pendant le traitement.

---

## Fonctionnalité 1 — Caméra automatique

### Problème V2

Dans la V2, l'utilisateur malvoyant devait :
1. Trouver et appuyer sur le bouton SCAN pour activer la caméra.
2. Attendre la confirmation vocale "Camera on."
3. Seulement ensuite, utiliser DESCRIBE ou TEXT.

Cette friction supplémentaire était inutile : dans 100 % des cas d'usage, l'utilisateur veut que la caméra soit active.

### Solution V3

La caméra démarre automatiquement dès que l'écran principal est affiché (`_enterMain()`). L'utilisateur entend directement "A-Eyes ready. Say describe, text, details, repeat or stop." et peut utiliser l'app immédiatement.

---

## Fonctionnalité 2 — Text (OCR)

### Cas d'usage

Ahmed, 58 ans, malvoyant. Il se trouve dans une rue et veut savoir sur quel tronçon il se trouve. Il pointe son téléphone vers un panneau de rue et dit «text». L'application lui répond «Rue du Général de Gaulle». Il peut aussi pointer vers une vitrine pour lire les horaires d'ouverture, un menu de restaurant, le nom d'un produit en magasin, le numéro d'un bus, etc.

### Comportement

1. L'utilisateur appuie sur **TEXT** (orange) ou dit «text».
2. L'app vocalise «Reading text...»
3. Un frame est capturé depuis le flux caméra.
4. L'image est envoyée à `/api/text`.
5. GPT-4.1-mini extrait tout le texte visible et le retourne tel quel.
6. Le TTS dicte le texte. Si aucun texte : «No text detected in the image.»

---

## Fonctionnalité 3 — Details

### Cas d'usage

L'utilisateur a obtenu une description globale avec DESCRIBE. Il veut en savoir plus (couleurs, positions, objets, texte visible) sans recapturer. Il appuie sur **DETAILS** ou dit «details».

### Comportement

1. DETAILS n'effectue pas de nouvelle capture — il utilise `_lastFrame` (image de la dernière analyse DESCRIBE ou TEXT).
2. Si aucune image n'a encore été capturée : «Please describe or read text first.»
3. L'image est envoyée à `/api/details`.
4. GPT-4.1-mini produit 4 à 6 phrases (scène, sujets, positions, couleurs, lumière, texte visible).
5. Le TTS lit la description détaillée.

### Différence DESCRIBE / DETAILS

| Feature | DESCRIBE | DETAILS |
|---------|----------|---------|
| Capture | Oui (nouvelle) | Non (réutilise `_lastFrame`) |
| Longueur | 1 phrase, < 20 mots | 2 à 3 phrases |
| Endpoint | `/api/describe` | `/api/details` |
| Objectif | Vue d'ensemble rapide | Analyse approfondie |
| max_tokens | 200 | 500 |

---

## Fonctionnalité 4 — Suppression de l'écran Settings

L'écran de réglages (vitesse TTS) a été supprimé pour simplifier l'interface. La vitesse par défaut (160 wpm) couvre l'ensemble des cas d'usage.

Fichiers impactés : `index.html`, `style.css`, `app.js`, `voice.js`.

---

## Fonctionnalité 5 — Anti-boucle vocale

### Problème

Le TTS prononce «Reading text...» et le micro capte le mot «text», redéclenchant la commande en boucle.

### Solution

La reconnaissance vocale est complètement arrêtée (`stopListening()`) dès le début du traitement (`_setBusy()`) et redémarrée uniquement dans le callback TTS final (`_setIdle()`). Aucun mot prononcé pendant le traitement ne peut être capturé ni bufférisé par Chrome.

La caméra n'est jamais affectée.

---

## Interface utilisateur — Disposition des boutons

```
┌────────────────────────────────────────────┐
│   [flux caméra live]                        │
│                                            │
├────────────────────────────────────────────┤
│           DESCRIBE (jaune)                │  ← pleine largeur
├──────────────┼───────────────┼──────────────┤
│ TEXT (orange) │ DETAILS (vert) │ ASK (violet) │  ← même hauteur (80px)
├──────────────┴───────────────┴──────────────┤
│           REPEAT (bleu)                   │
└────────────────────────────────────────────┘
```

## Commandes vocales

| Mot-clé | Action |
|---------|--------|
| describe | Capture + description globale (1 phrase) |
| text | Capture + lecture du texte visible |
| details | Description détaillée de la dernière image |
| ask | Pose une question sur la dernière image (voix) |
| repeat | Relit le dernier message TTS |
| stop | Interrompt la lecture TTS (caméra non affectée) |
| help | Énumère les commandes disponibles |

---

## Choix de conception

### Pourquoi GPT-4.1-mini pour l'OCR ?

Les services OCR classiques (Google Vision, Azure OCR) ont été écartés pour rester dans le stack existant (OpenAI déjà intégré en V2). GPT-4.1-mini avec un prompt orienté OCR produit des résultats comparables pour les cas d'usage visuels courants, sans nouvelle dépendance ni complexité d'intégration.

### Pourquoi DETAILS ne recapture pas ?

L'utilisateur a déjà orienté sa caméra pour DESCRIBE. Recapturer obligerait à maintenir la même position. Travailler sur `_lastFrame` garantit que DETAILS et ASK référencent exactement la même image.

---

## Fonctionnalité 6 — Retour haptique

`_setBusy()` déclenche `navigator.vibrate?.(80)` (80 ms — début de traitement). `_setIdle()` déclenche `navigator.vibrate?.([80, 60, 80])` (double vibration — fin de traitement). L'opérateur `?.` assure une dégradation gracieuse sur iOS (API non supportée).

---

## Fonctionnalité 7 — Désactivation des boutons pendant traitement

`_setBusy()` met tous les boutons d'action (`btn-describe`, `btn-text`, `btn-details`, `btn-ask`) en `disabled`. `_setIdle()` les réactive. L'utilisateur ne peut pas déclencher deux requêtes simultanées.

La V3 porte sur l'amélioration de l'expérience utilisateur avec deux évolutions fonctionnelles :

1. Suppression du bouton SCAN — la caméra s'ouvre automatiquement.
2. Nouvelle feature **Text** — détecte et dicte le texte visible dans l'image.

---

## Fonctionnalité 1 — Caméra automatique

### Problème V2

Dans la V2, l'utilisateur malvoyant devait :
1. Trouver et appuyer sur le bouton SCAN pour activer la caméra.
2. Attendre la confirmation vocale "Camera on."
3. Seulement ensuite, utiliser DESCRIBE ou TEXT.

Cette friction supplémentaire était inutile : dans 100 % des cas d'usage, l'utilisateur veut que la caméra soit active.

### Solution V3

La caméra démarre automatiquement dès que l'écran principal est affiché (`_enterMain()`). L'utilisateur entend directement "A-Eyes ready. Say describe, text, repeat, settings or stop." et peut utiliser l'app immédiatement.

Le bouton SCAN est supprimé. En cas d'échec de la caméra (permission refusée, matériel absent), un message vocal explicite est émis.

---

## Fonctionnalité 2 — Text (OCR)

### Cas d'usage

Ahmed, 58 ans, malvoyant. Il se trouve dans une rue et veut savoir sur quel tronçon il se trouve. Il pointe son téléphone vers un panneau de rue et dit "text". L'application lui répond "Rue du Général de Gaulle". Il peut aussi pointer vers une vitrine pour lire les horaires d'ouverture, un menu de restaurant, le nom d'un produit en magasin, le numéro d'un bus, etc.

### Comportement

1. L'utilisateur appuie sur le bouton **TEXT** (orange, #FF8C00) ou dit "text".
2. L'app vocalise "Reading text..." pour indiquer que le traitement est en cours.
3. Un frame est capturé depuis le flux caméra.
4. L'image est envoyée à `/api/text` (backend FastAPI).
5. GPT-4.1-mini extrait tout le texte visible et le retourne tel quel.
6. Le TTS dicte le texte à l'utilisateur.
7. Si aucun texte n'est visible : "No text detected in the image."

### Différence avec DESCRIBE

| Feature | DESCRIBE | TEXT |
|---------|----------|------|
| Objectif | Décrire la scène en langage naturel | Lire le texte visible tel quel |
| Prompt | "Describe this scene in 2–3 sentences" | "Read all visible text exactly as it appears" |
| Sortie typique | "A person is standing in front of a red building…" | "Rue du Général de Gaulle — Sens unique" |
| Longueur max | 200 tokens | 300 tokens |
| Usage principal | Comprendre l'environnement | Lire des panneaux, enseignes, étiquettes |

---

## Interface utilisateur V3

### Disposition des boutons (écran principal)

```
┌──────────────────────────┐
│   [flux caméra live]     │
│                          │
├──────────────────────────┤
│  DESCRIBE  (vert)        │
├──────────────────────────┤
│  TEXT      (orange)      │
├──────────────────────────┤
│  REPEAT    (bleu)        │
├──────────────────────────┤
│  SETTINGS  (gris)        │
└──────────────────────────┘
```

### Commandes vocales V3

| Mot-clé | Action |
|---------|--------|
| describe | Analyse la scène et la décrit |
| text | Lit le texte visible dans l'image |
| repeat | Relit le dernier message TTS |
| settings | Ouvre l'écran de réglages |
| stop | Arrête la caméra |
| help | Énumère les commandes disponibles |

---

## Choix de conception

### Pourquoi GPT-4.1-mini pour l'OCR ?

Les services OCR classiques (Google Vision, Azure OCR) ont été écartés pour rester dans le stack existant (OpenAI déjà intégré en V2). GPT-4.1-mini avec un prompt orienté OCR produit des résultats comparables pour les cas d'usage visuels courants, sans nouvelle dépendance ni complexité d'intégration.

Pour une version production avec des volumes élevés, une migration vers un service OCR dédié (moins coûteux par requête) reste envisageable sans modifier le frontend ni l'interface de l'endpoint.

### Pourquoi la couleur orange pour le bouton TEXT ?

Le thème existant utilise :
- Jaune (#FFCC00) — réservé aux focus outlines (accessibilité)
- Vert (#1AB34D) — DESCRIBE
- Bleu (#3399FF) — REPEAT
- Gris (#4D4D4D) — SETTINGS

L'orange (#FF8C00) offre un contraste suffisant sur fond noir (ratio > 3:1) et se distingue visuellement des autres boutons sans collision avec le système de couleurs existant.
