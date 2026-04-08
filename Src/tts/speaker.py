"""
speaker.py — Synthèse vocale (Text-To-Speech) via SAPI Windows.

Ce module fournit la classe Speaker qui utilise l'API SAPI (Speech API)
de Windows via la bibliothèque win32com pour lire du texte à voix haute.

Pourquoi SAPI plutôt que pyttsx3 ?
  - SAPI est natif Windows : plus stable, pas de dépendances supplémentaires.
  - pyttsx3 peut planter sous Windows à cause de conflits COM dans certains environnements.
  - win32com donne accès direct à l'objet SpVoice, ce qui permet un contrôle fin
    de la vitesse (Rate) et garantit la bonne initialisation COM par thread.

Architecture :
  - La synthèse vocale s'exécute dans un thread dédié (_worker) pour ne jamais
    bloquer le thread principal Kivy (interface graphique).
  - Les messages à lire sont transmis via une file d'attente thread-safe (queue.Queue).
"""

import queue          # File d'attente thread-safe pour les messages TTS
import threading      # Thread dédié à la synthèse vocale (évite de bloquer l'UI)
import pythoncom      # Initialisation COM obligatoire pour les objets win32com dans un thread
import win32com.client  # Accès à l'objet SAPI.SpVoice (Windows Speech API)
from config import TTS_RATE_DEFAULT  # Vitesse de parole par défaut (en mots/minute)

# Sentinel (objet unique) utilisé pour signaler au thread worker de s'arrêter.
# On utilise un objet Python ordinaire (pas None ni "") pour éviter toute ambiguïté.
_STOP = object()


class Speaker:
    """
    Synthèse vocale asynchrone via SAPI (Windows Speech API).

    Le texte à lire est mis en file d'attente et traité dans un thread dédié,
    de façon à ne jamais bloquer le thread principal de l'interface Kivy.

    Cycle de vie :
        speaker = Speaker()          # Le thread worker démarre automatiquement
        speaker.speak("Bonjour")     # Mise en file, lecture non bloquante
        speaker.set_rate(200)        # Changement de vitesse pour les prochains messages
        speaker.repeat()             # Relit le dernier message prononcé
    """

    def __init__(self):
        """
        Initialise la file d'attente, les attributs d'état,
        et démarre immédiatement le thread de synthèse vocale.
        """
        self._queue: queue.Queue = queue.Queue()  # File des messages en attente de lecture
        self._last_message: str = ""              # Dernier message prononcé (pour la fonction "répéter")
        self._rate: int = TTS_RATE_DEFAULT        # Vitesse courante en mots/minute
        # Thread daemon : s'arrête automatiquement quand l'application se ferme
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()  # Démarre le worker TTS en arrière-plan

    # ── API publique ──────────────────────────────────────────────────────────

    def speak(self, text: str):
        """
        Met un texte en file d'attente pour le lire à voix haute.
        Méthode non bloquante : retourne immédiatement.

        Args:
            text (str): Le texte à vocaliser.
        """
        self._last_message = text       # Sauvegarde pour la fonction "répéter"
        self._queue.put(text)           # Envoi au thread worker via la file

    def repeat(self):
        """
        Remet en file d'attente le dernier message prononcé.
        Ne fait rien si aucun message n'a encore été prononcé.
        """
        if self._last_message:
            self._queue.put(self._last_message)

    def set_rate(self, rate: int):
        """
        Modifie la vitesse de parole (en mots/minute).
        La nouvelle vitesse sera appliquée à partir du prochain message.

        Args:
            rate (int): Vitesse souhaitée, typiquement entre TTS_RATE_MIN et TTS_RATE_MAX.
        """
        self._rate = int(rate)

    # ── Thread SAPI ───────────────────────────────────────────────────────────

    def _worker(self):
        """
        Boucle principale du thread de synthèse vocale.

        Principe de fonctionnement :
          1. Initialise COM pour ce thread (obligatoire pour utiliser win32com).
          2. Crée l'objet SpVoice (moteur SAPI).
          3. Attend en boucle des messages dans la file.
          4. Pour chaque message, convertit la vitesse (mots/min → échelle SAPI),
             puis appelle voice.Speak() en mode bloquant.
          5. Se termine proprement si le sentinel _STOP est reçu.

        Note sur la conversion de vitesse :
          L'échelle SAPI va de -10 (très lent) à +10 (très rapide), 0 correspondant
          à environ 150 mots/minute. On applique la formule :
            sapi_rate = (vitesse_en_wpm - 150) / 10
          clampée entre -10 et +10.
        """
        # Initialisation COM : indispensable avant toute utilisation de win32com dans ce thread
        pythoncom.CoInitialize()
        try:
            # Création de l'objet SpVoice : moteur de synthèse vocale Windows
            voice = win32com.client.Dispatch("SAPI.SpVoice")

            while True:
                # Attente bloquante du prochain message dans la file (libère le CPU entre deux appels)
                text = self._queue.get()

                # Vérification du sentinel : si _STOP est reçu, on sort de la boucle proprement
                if text is _STOP:
                    break

                # Conversion de la vitesse mots/minute → échelle SAPI [-10, +10]
                # Exemple : 160 wpm → (160-150)//10 = 1  |  200 wpm → (200-150)//10 = 5
                sapi_rate = max(-10, min(10, (self._rate - 150) // 10))
                voice.Rate = sapi_rate  # Application de la vitesse à l'objet SAPI

                print(f"[TTS] Parle : {text!r}")
                voice.Speak(text)   # Lecture bloquante : attend la fin de la synthèse avant de continuer
                print("[TTS] Fin parole")

        finally:
            # Libération COM : toujours effectuer même en cas d'exception
            pythoncom.CoUninitialize()

