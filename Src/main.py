"""
main.py — Point d'entrée de l'application A-Eyes.

Ce module initialise le framework Kivy, charge le fichier de mise en page (.kv),
configure la journalisation (logging), et lance l'application.
L'application est destinée aux personnes malvoyantes : elle combine caméra,
synthèse vocale (TTS) et reconnaissance vocale dans une interface haute visibilité.
"""

import os       # Manipulation des chemins de fichiers système
import sys      # Manipulation du chemin d'importation Python (sys.path)
import logging  # Gestion des journaux (logs) de l'application

# ── Configuration des logs ────────────────────────────────────────────────────
# La bibliothèque comtypes (utilisée en interne par pyttsx3 sous Windows)
# génère énormément de messages DEBUG inutiles. On les réduit au niveau WARNING
# pour garder la console lisible.
logging.getLogger("comtypes").setLevel(logging.WARNING)

# ── Résolution des imports relatifs ──────────────────────────────────────────
# On insère le dossier contenant ce fichier (a_eyes/) en tête de sys.path
# afin que les imports comme "from camera.capture import ..." fonctionnent
# correctement, que le script soit lancé depuis n'importe quel répertoire.
sys.path.insert(0, os.path.dirname(__file__))

# ── Imports Kivy ─────────────────────────────────────────────────────────────
from kivy.app import App                                    # Classe de base de toute application Kivy
from kivy.lang import Builder                               # Moteur de chargement des fichiers .kv (mise en page déclarative)
from kivy.uix.screenmanager import ScreenManager, FadeTransition  # Gestionnaire d'écrans avec transition en fondu

# ── Imports des écrans de l'application ──────────────────────────────────────
from ui.main_screen import MainScreen          # Écran principal : caméra, TTS, commandes vocales
from ui.settings_screen import SettingsScreen  # Écran de réglages : vitesse de voix, volume

# ── Chargement du fichier de mise en page Kivy ───────────────────────────────
# Le fichier a_eyes.kv définit la disposition visuelle (widgets, styles, couleurs)
# de manière déclarative. Il est chargé une seule fois au démarrage.
# os.path.dirname(__file__) garantit un chemin absolu indépendant du répertoire courant.
Builder.load_file(os.path.join(os.path.dirname(__file__), "a_eyes.kv"))


class AEyesApp(App):
    """
    Classe principale de l'application Kivy.

    Hérite de App (kivy.app.App) qui gère la boucle événementielle,
    le cycle de vie de l'application (démarrage, pause, arrêt) et
    la communication entre les widgets.
    """

    # Titre affiché dans la barre de fenêtre sur desktop
    title = "A-Eyes"

    def build(self):
        """
        Méthode appelée automatiquement par Kivy au lancement.
        Construit et retourne le widget racine de l'application.

        Returns:
            ScreenManager : le gestionnaire d'écrans qui contient
                            tous les écrans de l'application.
        """
        # FadeTransition : transition en fondu entre les écrans (plus douce pour les malvoyants)
        sm = ScreenManager(transition=FadeTransition())

        # Ajout de l'écran principal (caméra + boutons d'action)
        sm.add_widget(MainScreen(name="main"))

        # Ajout de l'écran de réglages (vitesse TTS, volume)
        sm.add_widget(SettingsScreen(name="settings"))

        # Le ScreenManager affichera automatiquement le premier écran ajouté ("main")
        return sm


# ── Point d'entrée du script ─────────────────────────────────────────────────
# Ce bloc n'est exécuté que lorsque le fichier est lancé directement
# (python main.py), et non lorsqu'il est importé comme module.
if __name__ == "__main__":
    AEyesApp().run()  # Démarre la boucle événementielle Kivy
