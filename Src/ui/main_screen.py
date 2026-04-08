"""
main_screen.py — Écran principal de l'application A-Eyes.

Cet écran est le cœur de l'application. Il coordonne :
  - L'affichage du flux caméra en temps réel (widget Image Kivy)
  - Les quatre boutons d'action : SCAN, DÉCRIRE, RÉPÉTER, RÉGLAGES
  - La synthèse vocale (Speaker) pour guider l'utilisateur par audio
  - La reconnaissance vocale (VoiceListener) pour les commandes mains libres

Architecture multi-thread :
  - L'interface Kivy tourne dans le thread principal.
  - L'ouverture de la caméra est faite dans un thread secondaire (évite le gel de l'UI).
  - La reconnaissance vocale tourne dans son propre thread (VoiceListener).
  - La synthèse vocale (Speaker) possède son propre thread interne.
  - Toute modification de l'UI depuis un thread secondaire passe par Clock.schedule_once()
    pour être ré-exécutée dans le thread principal Kivy.
"""

from kivy.uix.screenmanager import Screen   # Classe de base pour un écran dans ScreenManager
from kivy.clock import Clock                 # Horloge Kivy : schedule_once/schedule_interval
import threading                             # Pour lancer l'ouverture de caméra en arrière-plan

from camera.capture import CameraCapture     # Gestion du flux vidéo OpenCV
from tts.speaker import Speaker              # Synthèse vocale SAPI Windows
from voice_input.listener import VoiceListener  # Reconnaissance vocale SpeechRecognition
from config import CAMERA_INDEX, CAMERA_FPS, DESCRIBE_STUB_MSG  # Constantes de configuration


class MainScreen(Screen):
    """
    Écran principal — 4 boutons : SCAN, DÉCRIRE, RÉPÉTER, RÉGLAGES.

    Hérite de Screen (kivy.uix.screenmanager.Screen).
    La disposition visuelle (boutons, aperçu caméra) est définie dans a_eyes.kv.
    Cette classe gère uniquement la logique : caméra, TTS, commandes vocales.

    Attributes:
        cam (CameraCapture): Objet de capture vidéo.
        tts (Speaker): Objet de synthèse vocale.
        voice (VoiceListener): Objet de reconnaissance vocale.
        _scanning (bool): True si le flux caméra est actif.
    """

    def __init__(self, **kwargs):
        """
        Initialise les composants principaux de l'écran.
        Appelé une seule fois au démarrage de l'application.

        Args:
            **kwargs: Arguments transmis à la classe parente Screen.
        """
        super().__init__(**kwargs)
        # Création de l'objet de capture caméra avec l'index et le FPS définis en config
        self.cam = CameraCapture(camera_index=CAMERA_INDEX, fps=CAMERA_FPS)
        # Création du moteur TTS — démarre son thread interne immédiatement
        self.tts = Speaker()
        # Création de l'écouteur vocal — on lui passe la méthode de rappel pour les commandes
        self.voice = VoiceListener(on_command=self._handle_voice_command)
        # État initial : la caméra est éteinte
        self._scanning = False

    # ── Cycle de vie écran ────────────────────────────────────────────────────

    def on_enter(self):
        """
        Appelé automatiquement par Kivy quand cet écran devient visible.
        Lance le message d'accueil et démarre l'écoute des commandes vocales.
        """
        # Message d'accueil audio pour indiquer à l'utilisateur que l'app est prête
        self.tts.speak("A-Eyes ready. Say scan, describe, repeat, settings or stop.")
        # Démarre le thread d'écoute micro en arrière-plan
        self.voice.start_listening()

    def on_leave(self):
        """
        Appelé automatiquement par Kivy quand on quitte cet écran (ex: vers réglages).
        Coupe la caméra et arrête l'écoute vocale pour économiser les ressources.
        """
        self._stop_camera()           # Libère la caméra et déprogramme le rafraîchissement
        self.voice.stop_listening()   # Arrête le thread de reconnaissance vocale

    # ── Actions boutons ───────────────────────────────────────────────────────

    def toggle_scan(self):
        """
        Bascule le flux caméra ON/OFF.
        Appelé par le bouton SCAN dans l'interface .kv.

        Si la caméra est éteinte → tente de l'ouvrir dans un thread séparé.
        Si la caméra est allumée → l'éteint immédiatement.
        """
        print("[BTN] SCAN clicked, scanning=", self._scanning)
        if not self._scanning:
            self.tts.speak("Starting camera...")
            # Ouverture dans un thread secondaire : cv2.VideoCapture peut prendre plusieurs secondes
            # Ce thread est daemon=True : il s'arrête automatiquement si l'application se ferme
            threading.Thread(target=self._start_camera_thread, daemon=True).start()
        else:
            self._stop_camera()
            self.tts.speak("Camera off.")

    def _start_camera_thread(self):
        """
        Exécuté dans un thread secondaire : tente d'ouvrir la caméra.
        Une fois le résultat connu, repasse dans le thread Kivy via Clock.schedule_once
        pour mettre à jour l'interface (une mise à jour UI depuis un thread non-Kivy est interdite).
        """
        ok = self.cam.start()  # Bloquant jusqu'à 8s (deux tentatives de 4s)
        print("[CAM] start() returned:", ok)
        # schedule_once garantit que _on_camera_started est appelé dans le thread principal Kivy
        Clock.schedule_once(lambda dt: self._on_camera_started(ok), 0)

    def _on_camera_started(self, ok: bool):
        """
        Appelé dans le thread principal Kivy après la tentative d'ouverture de caméra.
        Met à jour l'état et programme le rafraîchissement de la texture si succès.

        Args:
            ok (bool): True si la caméra a été ouverte avec succès.
        """
        if ok:
            self._scanning = True
            self.tts.speak("Camera on.")
            # schedule_interval appelle _update_frame toutes les (1/FPS) secondes
            Clock.schedule_interval(self._update_frame, 1 / CAMERA_FPS)
        else:
            self.tts.speak("Cannot open camera.")

    def on_describe(self):
        """
        Appelé par le bouton DÉCRIRE.
        En V0, l'analyse IA n'est pas disponible : on lit le message de substitution.
        En V1, cette méthode enverra la frame courante au modèle de vision.
        """
        print("[BTN] DESCRIBE clicked")
        # ── V0 : IA non connectée — message de substitution standard ──────────
        self.tts.speak(DESCRIBE_STUB_MSG)

    def on_help(self):
        """
        Appelé par le bouton AIDE (ou commande vocale "help").
        Lit la liste des commandes disponibles pour guider l'utilisateur.
        """
        self.tts.speak(
            "Available commands: "
            "Scan to start the camera. "
            "Describe to analyse the scene. "
            "Repeat to hear the last message again. "
            "Settings to adjust the voice. "
            "Stop to turn off the camera."
        )

    def on_repeat(self):
        """
        Appelé par le bouton RÉPÉTER.
        Demande au Speaker de relire le dernier message prononcé.
        """
        print("[BTN] REPEAT clicked, last_msg:", repr(self.tts._last_message))
        self.tts.repeat()

    def go_to_settings(self):
        """
        Navigue vers l'écran de réglages.
        self.manager est le ScreenManager parent, accessible depuis tout Screen.
        """
        self.manager.current = "settings"  # Change l'écran actif par son nom déclaré dans main.py

    # ── Commandes vocales ─────────────────────────────────────────────────────

    def _handle_voice_command(self, cmd: str):
        """
        Rappel (callback) appelé par VoiceListener depuis son thread d'écoute
        chaque fois qu'une commande vocale est reconnue.

        Associe chaque mot-clé reconnu à la méthode correspondante via un dictionnaire,
        puis planifie l'exécution dans le thread principal Kivy (Clock.schedule_once).

        Args:
            cmd (str): La commande reconnue (ex: "scan", "describe", "repeat"...).
        """
        # Table de correspondance commande vocale → méthode à appeler
        dispatch = {
            "scan":     self.toggle_scan,
            "describe": self.on_describe,
            "repeat":   self.on_repeat,
            "settings": self.go_to_settings,
            "help":     self.on_help,
            "stop":     self._stop_camera,
        }
        action = dispatch.get(cmd)  # Récupère la méthode associée (None si cmd inconnu)
        if action:
            # IMPORTANT : VoiceListener tourne dans un thread secondaire.
            # Kivy interdit les modifications de l'UI depuis un thread non-principal.
            # schedule_once place l'appel dans la file événementielle du thread Kivy.
            Clock.schedule_once(lambda dt: action(), 0)

    # ── Caméra interne ────────────────────────────────────────────────────────

    def _stop_camera(self):
        """
        Arrête le flux caméra et libère les ressources.
        - Déprogramme le rafraîchissement périodique des frames.
        - Libère l'objet VideoCapture OpenCV.
        - Remet le drapeau _scanning à False.
        """
        Clock.unschedule(self._update_frame)  # Annule les appels périodiques à _update_frame
        self.cam.stop()                        # Libère la ressource caméra OpenCV
        self._scanning = False

    def _update_frame(self, dt):
        """
        Appelé par l'horloge Kivy à chaque tick (environ 30 fois/seconde).
        Lit la frame courante de la caméra et l'affiche dans le widget Image (camera_view).

        Args:
            dt (float): Temps écoulé depuis le dernier appel (delta time, fourni par Kivy).
        """
        texture = self.cam.get_texture()  # Obtient la texture Kivy depuis la frame OpenCV
        if texture:
            # ids.camera_view : référence au widget Image défini dans a_eyes.kv avec id: camera_view
            self.ids.camera_view.texture = texture  # Met à jour l'affichage en temps réel
