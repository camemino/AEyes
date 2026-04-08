"""
listener.py — Reconnaissance vocale en continu pour A-Eyes.

Ce module fournit la classe VoiceListener qui écoute le microphone en arrière-plan
et détecte des commandes vocales prédéfinies en anglais.

Dépendances :
  - SpeechRecognition (speech_recognition) : abstraction de la reconnaissance vocale.
  - pyaudio : accès au microphone (requis par SpeechRecognition).
  - Connexion internet : Google Speech-to-Text est utilisé comme moteur de reconnaissance.

Conception dégradée (graceful degradation) :
  Si SpeechRecognition, pyaudio ou la connexion internet est manquante,
  la classe se désactive silencieusement. L'application reste 100% fonctionnelle
  via les boutons de l'interface — la voix est une fonctionnalité bonus.
"""

import threading  # Écoute dans un thread dédié pour ne jamais bloquer l'UI

# Importation conditionnelle : si le paquet n'est pas installé, on continue sans lui
try:
    import speech_recognition as sr   # Bibliothèque de reconnaissance vocale
    SR_AVAILABLE = True                # Flag : la reconnaissance vocale est disponible
except ImportError:
    SR_AVAILABLE = False               # Flag : désactivé silencieusement

# ── Table des commandes reconnues ──────────────────────────────────────────────
# Dictionnaire mot-clé → identifiant de commande.
# Le mot-clé est le mot anglais à détecter dans le texte reconnu.
# L'identifiant est la chaîne transmise au callback on_command.
# On pourrait simplifier (clé == valeur), mais cette structure facilite
# l'ajout futur de synonymes (ex: "camera" → "scan").
COMMANDS = {
    "scan":      "scan",       # Démarre/arrête la caméra
    "describe":  "describe",   # Analyse la scène (IA, V1)
    "repeat":    "repeat",     # Relit le dernier message
    "settings":  "settings",   # Navigue vers les réglages
    "help":      "help",       # Lit la liste des commandes
    "stop":      "stop",       # Arrête la caméra
}


class VoiceListener:
    """
    Écoute en continu le microphone et appelle un callback lors de la détection
    d'une commande vocale reconnue parmi les mots-clés définis dans COMMANDS.

    Architecture :
      - Un thread daemon unique exécute la boucle d'écoute.
      - Le moteur de reconnaissance est Google STT (nécessite internet).
      - En cas d'absence de micro, de SpeechRecognition ou de réseau,
        la classe se désactive proprement sans erreur.

    Attributes:
        available (bool): True si SpeechRecognition est installé et utilisable.
        _on_command: Callable(str) transmis au constructeur.
        _active (bool): True si la boucle d'écoute doit continuer.
        _thread: Thread d'écoute (None si non démarré).
    """

    def __init__(self, on_command):
        """
        Initialise l'écouteur vocal.

        Args:
            on_command (callable): Fonction appelée avec la clé de commande détectée
                                   (ex: "scan", "describe", "repeat", "settings", "stop").
                                   Cette fonction sera appelée depuis le thread d'écoute —
                                   l'appelant doit gérer le transfert vers le thread principal si besoin.
        """
        self._on_command = on_command   # Callback à appeler lors d'une commande reconnue
        self._active = False            # Contrôle de la boucle d'écoute
        self._thread = None             # Référence au thread d'écoute (initialisé dans start_listening)
        self.available = SR_AVAILABLE   # Indique si la fonctionnalité est disponible

    # ── API publique ──────────────────────────────────────────────────────────

    def start_listening(self):
        """
        Démarre la boucle d'écoute vocale dans un thread daemon.
        Ne fait rien si SpeechRecognition n'est pas disponible.
        """
        if not self.available:
            print("[VOICE] SpeechRecognition not available — voice commands disabled")
            return  # Dégradation silencieuse : l'app continue sans commandes vocales

        self._active = True
        # Thread daemon : s'arrête automatiquement si l'application se ferme
        self._thread = threading.Thread(
            target=self._listen_loop, daemon=True
        )
        self._thread.start()
        print("[VOICE] Listening started (en-US)")

    def stop_listening(self):
        """
        Demande l'arrêt de la boucle d'écoute.
        L'arrêt est asynchrone : le thread se terminera à la prochaine itération.
        """
        self._active = False  # Le thread vérifie ce flag à chaque tour de boucle

    # ── Interne ───────────────────────────────────────────────────────────────

    def _listen_loop(self):
        """
        Boucle d'écoute vocale principale. Tourne dans un thread dédié.

        Étapes :
          1. Création du Recognizer et du Microphone.
          2. Calibration du bruit ambiant (0,5 seconde).
          3. Boucle : écoute par tranches de 3 secondes, reconnait avec Google STT,
             cherche un mot-clé dans le texte reconnu et appelle le callback.
          4. Les erreurs réseau, silence, mot non reconnu sont ignorés silencieusement.
        """
        recognizer = sr.Recognizer()  # Objet de reconnaissance vocale SpeechRecognition

        try:
            mic = sr.Microphone()  # Accès au microphone système par défaut
        except Exception:
            # Aucun microphone disponible (périphérique absent ou non autorisé)
            self._active = False
            return

        with mic as source:
            # Calibration du niveau de bruit ambiant pour améliorer la détection
            # duration=0.5s : rapide mais suffisante dans un environnement calme
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("[VOICE] Mic calibrated, listening for commands...")

            while self._active:
                try:
                    # Écoute jusqu'à 3 secondes de silence (timeout) ou 3 secondes de parole (phrase_time_limit)
                    audio = recognizer.listen(
                        source, timeout=3, phrase_time_limit=3
                    )

                    # Envoi de l'audio au service Google Speech-to-Text
                    # language="en-US" : commandes en anglais américain
                    text = recognizer.recognize_google(
                        audio, language="en-US"
                    ).lower()  # Mise en minuscules pour simplifier la comparaison

                    print(f"[VOICE] Heard: '{text}'")

                    # Recherche du premier mot-clé connu dans le texte reconnu
                    for keyword, cmd in COMMANDS.items():
                        if keyword in text:
                            print(f"[VOICE] Command matched: {cmd}")
                            self._on_command(cmd)  # Appel du callback avec l'identifiant de commande
                            break  # On ne traite qu'une commande par écoute

                except sr.WaitTimeoutError:
                    pass  # Aucune parole détectée dans le délai — on reboucle normalement

                except sr.UnknownValueError:
                    pass  # Parole détectée mais non compréhensible — on reboucle

                except sr.RequestError:
                    pass  # Erreur réseau (Google STT inaccessible) — on continue sans planter

                except Exception:
                    pass  # Toute autre exception inattendue — on ignore pour rester robuste
