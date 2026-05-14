# A-Eyes — Guide utilisateur

## Présentation

A-Eyes est une application d'assistance visuelle accessible depuis un navigateur.  
Elle capture une image via la caméra, l'envoie à un modèle d'IA, puis restitue le résultat à voix haute.

---

## Prérequis

- Un navigateur moderne (Chrome ou Edge recommandés — Firefox ne supporte pas les commandes vocales).
- Accès à la caméra et au microphone autorisé par le navigateur.
- Connexion internet (l'IA est hébergée côté serveur).

---

## Démarrage

1. Ouvrez l'URL de l'application (ex : `https://a-eyes.onrender.com`) ou `http://localhost:8000` en local.
2. Acceptez les permissions caméra et microphone demandées par le navigateur.
3. Le flux vidéo s'affiche à l'écran — l'application est prête.

---

## Fonctions principales

### Boutons de l'écran principal

| Bouton | Commande vocale | Action |
|--------|----------------|--------|
| DESCRIBE | `describe` | Capture une photo et demande à l'IA une description globale de la scène (1 phrase, < 20 mots). |
| TEXT | `text` | Capture une photo et lit à voix haute le texte visible dans l'image. |
| DETAILS | `details` | Demande une description plus précise (2 à 3 phrases) de la dernière image capturée. |
| ASK | *(aucune)* | Pose une question vocale à l'IA sur la dernière image analysée. |
| REPEAT | `repeat` | Relit le dernier message prononcé. |

### Commandes vocales supplémentaires

| Mot-clé (en anglais) | Effet |
|----------------------|-------|
| `help` | Annonce les commandes disponibles. |
| `stop` | Arrête la lecture vocale en cours (la caméra reste active). |

> Les commandes vocales fonctionnent en écoute continue. Pendant une lecture TTS, seul `stop` est actif pour éviter que le micro capte la synthèse vocale.

---

## Disposition des boutons

```
[ DESCRIBE          (vert, pleine largeur) ]
[ TEXT ] [ DETAILS ] [ ASK ]   ← même hauteur
[ REPEAT            (bleu) ]
```

---

## Conseils d'utilisation

- Tenez l'appareil stable et orientez la caméra vers la scène avant d'appuyer sur DESCRIBE ou TEXT.
- Utilisez DESCRIBE pour une vue d'ensemble rapide, puis DETAILS pour obtenir plus d'informations sur la même image sans recapturer.
- En cas de mauvaise description, recommencez la capture — l'éclairage et la distance influencent la qualité.
- ASK permet des questions de suivi sur la dernière image sans recapturer.
- `stop` interrompt la lecture sans couper la caméra.
- Sur le plan hébergé gratuit (Render), le service peut prendre ~30 secondes à répondre après une période d'inactivité.

---

## Résolution de problèmes courants

| Symptôme | Solution |
|----------|----------|
| La caméra ne s'affiche pas | Vérifiez que la permission caméra est accordée dans les paramètres du navigateur. |
| Les commandes vocales ne fonctionnent pas | Utilisez Chrome ou Edge ; vérifiez la permission microphone. |
| L'app ne répond plus aux commandes vocales | Dites `stop` pour débloquer (la restriction vocale est levée automatiquement en fin de lecture). |
| Aucune réponse de l'IA | Vérifiez votre connexion internet ; si en local, vérifiez que `OPENAI_API_KEY` est configurée. |
