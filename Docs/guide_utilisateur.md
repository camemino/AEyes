# A-Eyes — Guide utilisateur

## Présentation

A-Eyes est une application d'assistance visuelle accessible depuis un navigateur.
Elle capture une image via la caméra, l'envoie à un modèle d'IA, puis restitue le résultat à voix haute.

Toutes les fonctions se pilotent au toucher ou à la voix — l'écran n'a pas besoin d'être vu.

---

## Prérequis

- Un navigateur moderne : Chrome ou Edge recommandés. Firefox ne supporte pas les commandes vocales (les boutons restent fonctionnels).
- Permissions caméra et microphone accordées au navigateur.
- Connexion internet (le traitement IA est effectué côté serveur).

---

## Démarrage

1. Ouvrez l'URL de l'application (ex. `https://a-eyes.onrender.com`) ou `http://localhost:8000` en local.
2. Acceptez les permissions caméra et microphone demandées par le navigateur.
3. Touchez une fois l'écran — cela active l'audio (obligatoire sur iPhone).
4. Le flux vidéo s'affiche et l'app annonce vocalement "A-Eyes ready." — elle est prête.

---

## Fonctions principales

### Boutons de l'écran principal

| Bouton | Couleur | Commande vocale | Action |
|--------|---------|----------------|--------|
| DESCRIBE | Vert | `describe` | Capture une photo et décrit la scène en une phrase (vue d'ensemble rapide). |
| TEXT | Orange | `text` | Capture une photo et lit tout le texte visible : panneaux, étiquettes, prix, menus… |
| DETAILS | Vert foncé | `details` | Description précise (2-3 phrases) de la dernière image capturée — positions, couleurs, lumière. |
| ASK | Violet | `ask` ou `ask <question>` | Pose une question à voix haute sur la dernière image. |
| FIND | Teal | `find <objet>` | Recherche un objet et guide vers lui en temps réel ("Turn right", "Straight ahead"…). |
| REPEAT | Bleu | `repeat` | Relit le dernier message prononcé. |

### Commandes vocales supplémentaires

| Mot-clé | Effet |
|---------|-------|
| `help` | Annonce toutes les commandes disponibles. |
| `stop` | Interrompt immédiatement la lecture vocale ou la recherche FIND en cours. La caméra reste active. |

> Les commandes vocales fonctionnent en écoute continue. Pendant une analyse ou une lecture TTS, seul `stop` est actif — le micro ne peut pas déclencher d'autre commande par accident.

---

## Disposition des boutons

```
[ DESCRIBE               (vert, pleine largeur) ]
[ TEXT ]  [ DETAILS ]  [ ASK ]    ← même hauteur
[ FIND                  (teal, pleine largeur) ]
[ REPEAT                (bleu) ]
```

---

## Mode FIND — recherche guidée d'objet

Le mode FIND analyse le flux caméra en boucle et guide vocalement vers l'objet cherché.

**Lancement**

- Par la voix : dites `find <objet>` — ex. `find my keys`, `find the red cup`, `find my phone`.
- Par le bouton FIND : l'app demande "What are you looking for ?" — répondez à voix haute.

**Guidage**

L'app indique la direction à suivre : `Turn right`, `Turn left`, `Straight ahead`, `Look up`, `Look down`, `Behind you`.
Quand l'objet est trouvé : double bip aigu + "Found it!".
Quand l'objet n'est pas visible : bip grave + "Not visible".

L'app ne répète un message que si la direction change — silence quand vous êtes sur la bonne trajectoire.

**Arrêt**

La session s'arrête automatiquement quand l'objet est trouvé, ou après 30 secondes.
Pour arrêter manuellement : dites `stop` ou tapez le bouton **STOP** rouge qui apparaît en plein écran pendant la recherche.

---

## Conseils d'utilisation

- Avant DESCRIBE ou TEXT, tenez l'appareil stable et orientez la caméra vers la scène.
- Utilisez DESCRIBE pour une vue d'ensemble, puis DETAILS pour approfondir la même image sans recapturer.
- ASK permet des questions de suivi sur la dernière image ("What colour is the door ?", "Is there any text ?").
- Pour FIND, bougez lentement et suivez les instructions — l'app parle seulement quand la direction change.
- Sur iPhone, touchez l'écran une fois avant de lancer une session FIND pour que les bips soient audibles.
- Sur le plan hébergé gratuit (Render), le service peut prendre ~30 secondes à répondre après une période d'inactivité — ouvrez l'app à l'avance.

---

## Résolution de problèmes courants

| Symptôme | Solution |
|----------|----------|
| La caméra ne s'affiche pas | Vérifiez que la permission caméra est accordée dans les paramètres du navigateur, puis rechargez la page. |
| Les commandes vocales ne fonctionnent pas | Utilisez Chrome ou Edge ; vérifiez la permission microphone. |
| L'app ne répond plus aux commandes vocales | Dites `stop` — cela libère l'écoute quelle que soit la situation. |
| Les bips FIND sont silencieux (iPhone) | Touchez une fois l'écran pour activer l'audio, puis relancez la recherche. |
| Le guidage FIND tourne en boucle sans trouver | L'objet est peut-être hors champ ou trop petit — balayez lentement la pièce. |
| Aucune réponse de l'IA | Vérifiez votre connexion internet. En local, assurez-vous que `OPENAI_API_KEY` est définie dans `backend/.env`. |
