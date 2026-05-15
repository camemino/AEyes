# Fonctionnalités V4 — A-Eyes

## Vue d'ensemble

La V4 ajoute une seule fonctionnalité majeure : le mode **FIND** — recherche guidée d'un objet par la voix.

L'utilisateur dit "find my keys" (ou "find red mug", "find my phone"…). L'application analyse le flux caméra en boucle et guide vocalement avec une notation horloge ("3 o'clock, mid", "straight ahead, close", "behind you") jusqu'à trouver l'objet, entendre "stop", ou atteindre 30 secondes de recherche.

Deux sons mono complètent le guidage vocal :
- Un double chirp aigu (800→1200 Hz) quand l'objet est trouvé.
- Un ton grave (220 Hz) quand l'objet n'est pas visible dans le champ.

---

## Fonctionnalité — Mode FIND

### Cas d'usage

Leila, 34 ans, malvoyante. Elle a posé ses clés quelque part dans le salon. Elle ouvre A-Eyes, dit "find my keys" et balaie lentement la pièce avec son téléphone. L'app lui dit "9 o'clock, far" — elle tourne à gauche. "9 o'clock, mid" — elle avance. "9 o'clock, close" — elle s'approche. Double chirp + "Found." — elle tend la main.

Aucun geste supplémentaire n'est nécessaire. Elle n'a pas besoin de voir l'écran pendant toute la recherche.

### Déclenchement

La session FIND se lance uniquement par commande vocale : **"find \<objet\>"**.

Exemples : "find my keys", "find the red cup", "find my phone", "find glasses".

Toute phrase contenant le mot "find" suivi d'un texte est acceptée. L'objet peut être décrit librement : couleur, forme, nom générique ou spécifique.

### Guidage vocal — notation horloge

Le modèle répond avec une position en notation horloge (12 = devant, 3 = droite, 9 = gauche, 6 = sol) et une distance (close, mid, far). L'app prononce la phrase uniquement si elle diffère de la précédente — silence quand l'utilisateur est sur la bonne trajectoire.

| Position dite | Signification |
|---------------|---------------|
| "12 o'clock, close" | Droit devant, à portée |
| "3 o'clock, mid" | À droite, distance moyenne |
| "9 o'clock, far" | À gauche, loin |
| "behind you" | Derrière l'utilisateur |
| "I don't see it" | Objet hors champ |
| "Found." | Centré et à portée — session terminée |

### Bips mono

- Bip aigu (double chirp) : objet trouvé.
- Bip grave : objet hors champ ("lost").
- Pas de son pendant le guidage directionnel — la voix suffit.

Fonctionnent sur n'importe quel haut-parleur mono. Aucun matériel additionnel requis.

### Conditions d'arrêt

| Condition | Comportement |
|-----------|-------------|
| `clock = "found"` et `distance ≠ "far"` | Double chirp + TTS "Found." + fermeture session |
| Commande vocale "stop" | TTS "Search cancelled." + fermeture session |
| Clic sur bouton STOP plein écran | TTS "Search cancelled." + fermeture session |
| Timeout 30 s sans succès | TTS "I cannot find it." + fermeture session |

### Overlay STOP

Pendant toute la session FIND, un overlay plein écran noir 85 % apparaît avec :
- La phrase "Searching for \<objet\>…" en jaune.
- Un bouton **STOP** rouge géant (80 % de la largeur, 140 px de hauteur) pour permettre un arrêt immédiat au toucher, même sans voir l'écran.

L'overlay disparaît automatiquement à la fin de la session.

---

## Comportement de la boucle de guidage

1. L'app vocalise "Looking for \<objet\>." et démarre la boucle.
2. À chaque itération :
   - Le frame courant est capturé et downscalé à 512 px JPEG 0.7.
   - Envoyé à `POST /api/find` avec le nom de l'objet.
   - Le backend retourne un JSON : `{clock, distance, text, confidence}`.
   - Si l'objet est trouvé (`clock = "found"`, `distance ≠ "far"`) : bip aigu + "Found." + arrêt.
   - Si l'objet est hors champ (`clock = "lost"`) : bip grave.
   - Si la phrase `text` est différente de la précédente : TTS.
   - Si la phrase est identique : silence + délai 400 ms.
3. L'itération suivante commence uniquement après la fin du TTS (chaînage) → pas de superposition vocale.

---

## Intégration dans l'interface existante

Le mode FIND ne modifie pas l'interface principale. Les 5 boutons existants (DESCRIBE, TEXT, DETAILS, ASK, REPEAT) restent inchangés. L'overlay STOP est masqué par défaut et n'occupe aucun espace visuel au repos.

La commande "help" est mise à jour pour mentionner "find" :

> "Available commands: describe, text, details, ask, repeat, stop, find."

---

## Limites connues

| Limite | Détail |
|--------|--------|
| Un seul objet à la fois | La session FIND recherche un seul objet. Pour en chercher un autre, relancer avec une nouvelle commande. |
| Objets très petits ou partiellement visibles | Le modèle peut ne pas détecter un objet très petit ou largement hors champ. L'app dit "I don't see it." |
| Hallucination "found" | Le modèle peut se tromper. Mitigation : le succès n'est accepté que si `distance ≠ "far"`. |
| iOS Safari + AudioContext | Les bips nécessitent un geste utilisateur préalable (tap sur l'écran). L'app initialise l'AudioContext au premier tap global. Sans tap préalable, les bips sont silencieux mais le guidage vocal fonctionne. |
| Environnement bruyant | La commande vocale "find \<objet\>" peut être mal reconnue. Plan B : formuler lentement et clairement. |
