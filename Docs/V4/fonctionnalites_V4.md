# Fonctionnalités V4 — A-Eyes

## Vue d'ensemble

La V4 ajoute une seule fonctionnalité majeure : le mode **FIND** — recherche guidée d'un objet par la voix.

L'utilisateur dit "find my keys" (ou "find red mug", "find my phone"…). L'application analyse le flux caméra en boucle et guide vocalement avec des instructions directionnelles ("Turn right", "Straight ahead, almost there", "Behind you"…) jusqu'à trouver l'objet, entendre "stop", ou atteindre 30 secondes de recherche.

Trois sons mono complètent le guidage vocal (oscillateur de type `square`, bien audible sur les petits haut-parleurs de téléphone) :
- Un bip court neutre (520 Hz 80 ms) quand une photo est prise et analysée.
- Un double bip aigu (880 Hz puis 1320 Hz) quand l'objet est trouvé.
- Un ton grave descendant (300→220 Hz) quand l'objet n'est pas visible dans le champ.

---

## Fonctionnalité — Mode FIND

### Cas d'usage

Leila, 34 ans, malvoyante. Elle a posé ses clés quelque part dans le salon. Elle ouvre A-Eyes, dit "find my keys" et balaie lentement la pièce avec son téléphone. L'app lui dit "Turn left" — elle tourne. "Straight ahead, keep going" — elle avance. "Straight ahead, almost there" — elle s'approche. Double bip + "Found it!" — elle tend la main.

Aucun geste supplémentaire n'est nécessaire. Elle n'a pas besoin de voir l'écran pendant toute la recherche.

### Déclenchement

La session FIND se lance uniquement par commande vocale : **"find \<objet\>"**.

Exemples : "find my keys", "find the red cup", "find my phone", "find glasses".

Toute phrase contenant le mot "find" suivi d'un texte est acceptée. L'objet peut être décrit librement : couleur, forme, nom générique ou spécifique.

### Guidage vocal — instructions directionnelles

Le modèle retourne une direction et une distance. L'app prononce l'instruction associée uniquement si elle diffère de la précédente — silence quand l'utilisateur est sur la bonne trajectoire.

| Instruction dite | Signification |
|-----------------|---------------|
| "Turn right" | L'objet est sur la droite |
| "Turn left" | L'objet est sur la gauche |
| "Straight ahead, keep going" | Droit devant, distance moyenne |
| "Straight ahead, almost there" | Droit devant, presque à portée |
| "Behind you" | L'objet est derrière l'utilisateur |
| "Look up" | L'objet est au-dessus |
| "Look down" | L'objet est en dessous |
| "Not visible" | Objet hors champ |
| "Found it!" | Centré et à portée — session terminée |

### Bips mono (onde carrée)

- Bip court neutre (520 Hz) : photo prise, analyse en cours.
- Double bip aigu (880 Hz + 1320 Hz) : objet trouvé.
- Bip grave descendant (300→220 Hz) : objet hors champ.

Fonctionnent sur n'importe quel haut-parleur mono. L'onde carrée est choisie pour ses harmoniques riches, bien reproduites par les petits haut-parleurs de téléphone.

### Conditions d'arrêt

| Condition | Comportement |
|-----------|-------------|
| `direction = "found"` et `distance ≠ "far"` | Double bip aigu + TTS "Found it!" + fermeture session |
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
   - Un bip neutre (520 Hz) indique que la photo a été prise.
   - Envoyé à `POST /api/find` avec le nom de l'objet.
   - Le backend retourne un JSON : `{direction, distance, text, confidence}`.
   - Si l'objet est trouvé (`direction = "found"`, `distance ≠ "far"`) : double bip aigu + "Found it!" + arrêt.
   - Si l'objet est hors champ (`direction = "not_visible"`) : bip grave descendant.
   - Si la phrase `text` est différente de la précédente : TTS.
   - Si la phrase est identique : silence + délai 400 ms.
3. L'itération suivante commence uniquement après la fin du TTS (chaînage) → pas de superposition vocale.

---

## Intégration dans l'interface existante

Le mode FIND ne modifie pas l'interface principale. Les 5 boutons (DESCRIBE, TEXT, DETAILS, ASK, FIND) et le bouton REPEAT occupent maintenant tout l'écran — l'affichage du flux caméra a été supprimé (inutile pour un malvoyant). L'overlay STOP est masqué par défaut et n'occupe aucun espace visuel au repos.

La commande "help" est mise à jour pour mentionner "find" :

> "Available commands: describe, text, details, ask, repeat, stop, find."

---

## Limites connues

| Limite | Détail |
|--------|--------|
| Un seul objet à la fois | La session FIND recherche un seul objet. Pour en chercher un autre, relancer avec une nouvelle commande. |
| Objets très petits ou partiellement visibles | Le modèle peut ne pas détecter un objet très petit ou largement hors champ. L'app dit "I don't see it." |
| Hallucination "found" | Le modèle peut se tromper. Mitigation : le succès n'est accepté que si `distance ≠ "far"`. |
| iOS Safari + AudioContext | Les bips nécessitent un geste utilisateur préalable (tap sur l'écran). Sans tap préalable, les bips sont silencieux mais le guidage vocal fonctionne. |
