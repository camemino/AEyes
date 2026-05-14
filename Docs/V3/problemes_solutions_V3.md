# Problèmes rencontrés et solutions — V3

---

## P-01 — Boucle infinie sur les commandes vocales

### Symptôme
Appuyer sur TEXT ou DESCRIBE déclenchait une boucle : le TTS prononçait "Reading text..." ou "Analysing scene...", le micro captait le mot-clé ("text", "describe"), et relançait la commande indéfiniment.

### Cause
La reconnaissance vocale restait active pendant toute la lecture TTS. Les mots prononcés par la synthèse étaient captés et interprétés comme des commandes.

### Solution (en deux étapes)

Étape 1 — Restriction pendant le TTS (`voice.js`, `tts.js`, `app.js`) :
- Ajout de `restrict()` / `unrestrict()` dans `VoiceListener`. En mode restreint, seul le mot-clé "stop" est accepté.
- Ajout des hooks `onBeforeSpeak` / `onAfterSpeak` dans `Speaker` pour appeler automatiquement `restrict()` / `unrestrict()` à chaque lecture.

Étape 2 — Flag `_processing` (`app.js`) :
- Le hook `onAfterSpeak` levait la restriction après le TTS intermédiaire ("Reading text..."), avant que l'API ait répondu. Le micro captait alors la réponse de l'IA et relançait la commande.
- Ajout du flag `_processing` : mis à `true` dès le début du handler, remis à `false` juste avant le `speak()` final. `onAfterSpeak` ne lève la restriction que si `_processing === false`.
- La restriction couvre ainsi tout le cycle : TTS intermédiaire + appel API + TTS final.
Étape 3 — Solution finale : `stopListening`/`startListening` (`app.js`, `voice.js`) :
- Les étapes 1 et 2 étaient insuffisantes sur Chrome : le navigateur bufférise les résultats de reconnaissance captés pendant le TTS et les livre après `unrestrict()`, contournant le filtrage dans `_handleResult()`.
- Solution définitive : `_setBusy()` appelle `stopListening()` (arrêt complet du moteur) ; `_setIdle()` appelle `startListening()` uniquement dans le callback du TTS final. Aucun résultat ne peut être bufférisé quand le moteur est à l'arrêt.
- `restrict()`/`unrestrict()` et `_processing` sont devenus obsolètes dans `app.js`.
---

## P-02 — La commande "stop" coupait la caméra

### Symptôme
Dire "stop" pour interrompre une lecture TTS éteignait aussi le flux caméra.

### Cause
La commande `stop` appelait `_stopCamera()` en plus du `tts.cancel()`.

### Solution
La commande `stop` appelle uniquement `tts.cancel()` (qui lève aussi la restriction vocale via `onAfterSpeak`). La caméra n'est jamais touchée.

---

## P-03 — `onAfterSpeak` non déclenché lors d'un cancel()

### Symptôme
Appeler `tts.cancel()` interrompait la lecture mais ne levait pas la restriction vocale, bloquant les commandes suivantes.

### Cause
`speechSynthesis.cancel()` n'émet pas l'événement `onend` sur l'utterance en cours — le hook `onAfterSpeak` n'était donc jamais appelé.

### Solution
La méthode `cancel()` ajoutée dans `Speaker` appelle explicitement `this.onAfterSpeak?.()` après `speechSynthesis.cancel()`.

---

## P-04 — Prompts dispersés dans chaque endpoint

### Symptôme
Modifier le comportement du modèle obligeait à ouvrir 4 fichiers différents (`describe.py`, `details.py`, `text.py`, `ask.py`).

### Solution
Centralisation de tous les prompts dans `backend/prompts.py`. Chaque endpoint importe uniquement sa constante (`DESCRIBE_PROMPT`, `DETAILS_PROMPT`, `TEXT_PROMPT`, `ASK_PROMPT`).

---

## P-05 — DETAILS recapturait l'image au lieu de réutiliser la dernière

### Symptôme
Le bouton DETAILS prenait un nouveau frame caméra au lieu d'analyser l'image déjà capturée par DESCRIBE ou TEXT, ce qui forçait l'utilisateur à maintenir la même position.

### Solution
`onDetails()` utilise `_lastFrame` (le dernier frame capturé par DESCRIBE ou TEXT). Si aucune image n'a encore été capturée, un message vocal invite l'utilisateur à lancer DESCRIBE ou TEXT d'abord. Même comportement que ASK.

---

## P-06 — DESCRIBE donnait trop de détails

### Symptôme
La réponse de DESCRIBE était trop longue (2-3 phrases avec des listes d'objets), peu adaptée à une lecture TTS rapide pour un usage mobile.

### Solution
Prompt réduit à 1 phrase courte (< 20 mots) décrivant uniquement le lieu et l'action principale. Les détails sont réservés à DETAILS.

---

## P-07 — DETAILS donnait également trop de détails

### Symptôme
Avec 4 à 6 phrases demandées, la réponse était trop longue pour une utilisation courante.

### Solution
Prompt ajusté à 2-3 phrases couvrant les sujets principaux, leurs positions et un ou deux détails notables (couleur, lumière, texte visible).

---

## P-08 — Positions des objets exprimées côté caméra et non côté utilisateur

### Symptôme
Le modèle décrivait les positions du point de vue de l'image ("à gauche de l'image") plutôt que du point de vue de l'utilisateur qui tient le téléphone.

### Solution
Ajout de la consigne dans les prompts DESCRIBE, DETAILS et ASK : "Always describe positions from the user's point of view (left, right, in front, behind, above, below)."

---

## P-09 — Buffering Chrome : résultats vocaux livrés après unrestrict()

### Symptôme
Malgré l'implémentation de `restrict()`/`unrestrict()` et du flag `_processing`, la boucle vocale persistait sur Chrome : le mot "text" ou "describe" prononcé par le TTS déclenchait à nouveau la commande après la fin de la lecture.

### Cause
Chrome bufférise les résultats de la reconnaissance vocale en interne. Les résultats captés pendant que `_restricted = true` sont stockés et livrés à `_handleResult()` dès que la restriction est levée (`unrestrict()`). Le filtrage dans `_handleResult()` était donc contornué.

### Solution
Arrêt complet du moteur de reconnaissance (`stopListening()` → `recognition.stop()`) pendant tout traitement. Le moteur est redémarré (`startListening()`) uniquement dans le callback du TTS final, quand la synthèse est terminée et que le micro peut écouter sans risque. Aucun buffering n'est possible quand le moteur est arrêté.

---

## P-10 — Absence de retour utilisateur pendant traitement

### Symptôme
Pendant l'analyse (appel API + TTS), l'utilisateur ne savait pas si l'app traitait ou était bloquée. Il pouvait aussi appuyer plusieurs fois sur un bouton, générant plusieurs requêtes simultanées.

### Solution
- Retour haptique : `navigator.vibrate?.(80)` au début du traitement (`_setBusy()`), `navigator.vibrate?.([80, 60, 80])` à la fin (`_setIdle()`).
- Désactivation des boutons pendant le traitement : `_actionBtns.forEach(b => b.disabled = true)` dans `_setBusy()`, réactivation dans `_setIdle()`.
- L'opérateur `?.` assure une dégradation gracieuse sur iOS (API Vibration non supportée).
