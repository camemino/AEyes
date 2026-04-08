"""
settings_screen.py — Écran de réglages de l'application A-Eyes.

Cet écran permet à l'utilisateur de personnaliser les paramètres de synthèse vocale :
  - Vitesse de parole (slider de TTS_RATE_MIN à TTS_RATE_MAX mots/minute)

L'accès au Speaker (moteur TTS) se fait via le ScreenManager :
  self.manager.get_screen("main").tts
Cela évite une dépendance directe entre les deux écrans et garde l'architecture propre.
"""

from kivy.uix.screenmanager import Screen   # Classe de base pour un écran Kivy
from kivy.clock import Clock                 # Pour différer légèrement la navigation retour

from config import TTS_RATE_MIN, TTS_RATE_MAX, TTS_RATE_DEFAULT  # Plage et valeur initiale du slider


class SettingsScreen(Screen):
    """
    Écran de réglages — permet d'ajuster la vitesse de la synthèse vocale.

    Le widget slider (rate_slider) est défini dans a_eyes.kv et identifié par
    son id "rate_slider". Sa valeur va de TTS_RATE_MIN à TTS_RATE_MAX.

    L'accès au Speaker se fait en allant chercher l'écran "main" dans le ScreenManager,
    ce qui garantit qu'on utilise le même objet Speaker que l'écran principal.
    """

    def on_enter(self):
        """
        Appelé automatiquement par Kivy à chaque fois que l'écran devient visible.

        Actions :
          1. Annonce l'écran de réglages via la synthèse vocale.
          2. Initialise le slider à la valeur par défaut (TTS_RATE_DEFAULT).
        """
        speaker = self._get_speaker()
        if speaker:
            # Annonce audio : informe l'utilisateur de son emplacement et de la commande disponible
            speaker.speak("Settings screen. Use the slider to adjust the speech rate.")

        # Positionne le curseur du slider sur la valeur par défaut à chaque ouverture
        # (évite qu'un réglage résiduel d'une session précédente soit affiché incorrectement)
        self.ids.rate_slider.value = TTS_RATE_DEFAULT

    def on_rate_change(self, value: float):
        """
        Appelé automatiquement par le slider chaque fois que sa valeur change.
        Transmet la nouvelle vitesse au Speaker en temps réel.

        Args:
            value (float): Nouvelle valeur du slider (entre TTS_RATE_MIN et TTS_RATE_MAX).
                           Kivy passe une valeur float, on la convertit en int dans Speaker.
        """
        speaker = self._get_speaker()
        if speaker:
            speaker.set_rate(int(value))  # Applique la nouvelle vitesse pour les prochains messages

    def go_back(self):
        """
        Appelé par le bouton "Retour" de l'interface.

        Lit d'abord un message de confirmation ("Réglages sauvegardés"),
        puis attend 0,8 seconde avant de revenir à l'écran principal.
        Ce délai est nécessaire pour que le TTS ait le temps de commencer
        sa lecture avant que l'écran ne disparaisse.
        """
        speaker = self._get_speaker()
        if speaker:
            speaker.speak("Settings saved.")
        # Délai court pour laisser le TTS commencer avant la navigation
        Clock.schedule_once(lambda dt: self._do_back(), 0.8)

    def _do_back(self):
        """
        Effectue la navigation retour vers l'écran principal.
        Séparé de go_back() pour pouvoir être appelé via Clock.schedule_once.
        """
        self.manager.current = "main"  # Change l'écran actif par son nom déclaré dans main.py

    def _get_speaker(self):
        """
        Récupère l'objet Speaker depuis l'écran principal.

        Cette approche (accès via le ScreenManager) évite une injection de dépendance
        complexe et fonctionne car les deux écrans partagent le même ScreenManager.

        Returns:
            Speaker | None: L'objet Speaker si disponible, None en cas d'erreur.
                            Retourner None permet aux appelants de gérer l'absence proprement.
        """
        try:
            # Remonte au ScreenManager, récupère l'écran "main", puis son attribut tts
            return self.manager.get_screen("main").tts
        except Exception:
            # Sécurité : si le ScreenManager ou l'écran "main" n'est pas encore disponible
            # (ex: pendant l'initialisation), on retourne None sans lever d'exception.
            return None
