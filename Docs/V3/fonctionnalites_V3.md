# Fonctionnalités V3 — A-Eyes

## Vue d'ensemble

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
