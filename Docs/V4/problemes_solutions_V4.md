# Problèmes rencontrés et solutions — V4

---

## P-01 — Bips stéréo non audibles sur téléphone mono

### Symptôme
Le design initial prévoyait des bips stéréo directionnels : pan à gauche (-1) pour indiquer "gauche", pan à droite (+1) pour "droite". Sur un téléphone avec un seul haut-parleur, l'effet de panoramique est inaudible — tous les sons semblent identiques.

### Cause
L'API Web Audio `StereoPannerNode` fonctionne sur des sorties stéréo. Un haut-parleur mono mixe les deux canaux et annule l'information de position.

### Solution
Suppression du `StereoPannerNode`. Remplacement par 2 sons mono universels :
- Bip aigu (double chirp 800→1200 Hz) = succès ("found").
- Bip grave (220→180 Hz) = objet hors champ ("lost").

La position est portée uniquement par la voix (notation horloge). Cette approche fonctionne sur tout haut-parleur, sans matériel additionnel.

---

## P-02 — iOS Safari : AudioContext silencieux sans geste utilisateur

### Symptôme
Sur iOS Safari, l'`AudioContext` est créé en état `suspended` si aucun geste utilisateur n'a eu lieu. Les méthodes `beepFound()` et `beepLost()` ne produisaient aucun son.

### Cause
La politique Apple interdit la création ou le démarrage automatique d'un `AudioContext` sans interaction utilisateur explicite (tap, clic, toucher).

### Solution
L'`AudioContext` est initialisé (`beeper.init()`) dans un listener `pointerdown` sur `document`, déclenché une seule fois au premier tap global :

```js
const initAudio = () => {
  this._beeper.init();
  document.removeEventListener('pointerdown', initAudio);
};
document.addEventListener('pointerdown', initAudio, { once: true });
```

De plus, `FindSession` appelle `beeper.resume()` à chaque démarrage de session, pour reprendre un contexte suspendu après inactivité.

En pratique : l'utilisateur tape une fois n'importe où sur l'écran (ex. pour autoriser la caméra) — l'`AudioContext` est prêt pour le reste de la session.

---

## P-03 — Boucle trop bavarde : TTS redéclenché à chaque itération

### Symptôme
Avec un TTS prononcé à chaque appel `/api/find`, l'app répétait indéfiniment "3 o'clock, mid" même quand l'utilisateur était sur la bonne trajectoire. La voix recouvrait la réponse suivante, rendant le guidage illisible.

### Cause
Absence de mécanisme de déduplication des messages vocaux.

### Solution
Champ `_lastSpoken` dans `FindSession` : le TTS n'est prononcé que si `text !== _lastSpoken`. Quand la direction ne change pas, l'app est silencieuse (délai 400 ms entre itérations). La voix parle uniquement lors d'un changement de direction ou de distance — plus naturel, moins intrusif.

---

## P-04 — Hallucination "found" à longue distance

### Symptôme
Le modèle retournait `clock: "found"` alors que l'objet était visible mais loin (ex. à l'autre bout d'une pièce). La session se fermait prématurément.

### Cause
Le modèle interprète "l'objet est visible et centré" comme "found" sans tenir compte de la distance.

### Solution
La condition de succès dans `FindSession._loop()` exige à la fois `clock === "found"` ET `distance !== "far"` :

```js
if (clock === 'found' && distance !== 'far') {
  this._beeper.beepFound();
  this._tts.speak('Found.', () => this._onDone());
  return;
}
```

L'objet doit être centré ET proche/mi-distance pour que la session se termine.

---

## P-05 — Latence élevée sur `/api/find` avec images haute résolution

### Symptôme
Les appels à `/api/find` prenaient 2 à 3 secondes avec les images natives capturées par `camera.js` (JPEG 0.85, résolution complète), rendant le guidage lent et peu réactif.

### Cause
Les images natives peuvent peser 200 à 400 KB. Avec `detail: "auto"`, le modèle de vision tokenise l'image en haute résolution.

### Solution en deux étapes :

1. Côté modèle : `detail: "low"` dans l'appel OpenAI. Le modèle utilise une vignette 512×512 (~85 tokens d'image fixe) au lieu de tuiles haute résolution.

2. Côté client : downscale préalable à 512 px de large, JPEG 0.7, via canvas dans `find.js` (sans toucher `camera.js` qui sert aussi à DESCRIBE, TEXT et ASK) :

```js
async function _downscale(dataURL) {
  const ratio = Math.min(1, FRAME_WIDTH / img.width);
  canvas.getContext('2d').drawImage(img, 0, 0, w, h);
  return new Promise(resolve => {
    canvas.toBlob(b => resolve(b), 'image/jpeg', FRAME_QUALITY);
  });
}
```

Résultat : images < 40 KB, latence < 1.5 s en conditions normales.

---

## P-06 — Boutons d'action accessibles pendant une session FIND

### Symptôme
Pendant une session FIND, les boutons DESCRIBE, TEXT, DETAILS, ASK restaient actifs (car `_setBusy()` les désactive mais `_setIdle()` les réactive avant la fin de la session). Un clic sur DESCRIBE démarrait un second appel API en parallèle.

### Cause
`_setBusy()` / `_setIdle()` gèrent l'état des boutons, mais une session FIND est plus longue qu'un appel unique. `_setIdle()` était appelé à tort entre deux itérations.

### Solution
`_setBusy()` est appelé une seule fois au démarrage de la session. `_setIdle()` est appelé uniquement dans le callback `onDone` de `FindSession` (fin de session). L'overlay STOP masque visuellement tout l'écran principal pendant la recherche.

De plus, dans `_handleCommand`, pendant une session FIND active (`this._findSession !== null`), seule la commande "stop" est traitée — toutes les autres commandes vocales sont ignorées.

---

## P-07 — Bug CSS préexistant : `.btn-repeat` sans sélecteur

### Symptôme
Le bouton REPEAT n'était pas stylisé correctement (fond et hauteur non appliqués). La console CSS signalait des propriétés orphelines.

### Cause
Le sélecteur `.btn-repeat {` était manquant dans `style.css` : les propriétés `background`, `color`, `height` et `font-size` étaient déclarées sans sélecteur, produisant des erreurs de parsing CSS.

### Solution
Ajout du sélecteur `.btn-repeat` lors de l'insertion des styles de l'overlay FIND, corrigeant le bug au passage.
