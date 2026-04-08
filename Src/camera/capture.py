"""
capture.py — Gestion du flux vidéo de la caméra.

Ce module fournit la classe CameraCapture qui encapsule OpenCV (cv2) pour :
  - Ouvrir la caméra de façon robuste (avec timeout et repli sur un second backend)
  - Lire les images (frames) en temps réel
  - Convertir chaque image en texture Kivy pour l'affichage dans l'interface graphique
  - Libérer proprement les ressources à la fermeture

Séquence typique d'utilisation :
    cam = CameraCapture(camera_index=0, fps=30)
    if cam.start():
        texture = cam.get_texture()   # à appeler à chaque tick d'horloge
    cam.stop()
"""

import cv2                              # OpenCV : capture et traitement vidéo
import threading                        # Ouverture de caméra dans un thread séparé (évite le gel de l'UI)
from typing import Optional             # Type hint : indique qu'une valeur peut être None
from kivy.graphics.texture import Texture  # Objet texture Kivy : permet d'afficher une image dans un widget


class CameraCapture:
    """
    Gère le flux caméra via OpenCV et produit des textures Kivy.

    Attributes:
        camera_index (int): Indice de la caméra système à utiliser (0 = caméra principale).
        fps (int): Nombre d'images par seconde souhaité pour la capture.
        _cap: Objet VideoCapture d'OpenCV, ou None si la caméra n'est pas ouverte.
    """

    def __init__(self, camera_index: int = 0, fps: int = 30):
        """
        Initialise les paramètres de capture sans ouvrir la caméra.
        L'ouverture réelle se fait via start().

        Args:
            camera_index (int): Indice de la caméra à utiliser (défaut : 0).
            fps (int): Nombre d'images par seconde souhaité (défaut : 30).
        """
        self.camera_index = camera_index
        self.fps = fps
        self._cap = None   # Objet VideoCapture — initialisé à None jusqu'à l'appel de start()

    # ── Cycle de vie ───────────────────────────────────────────────────────── 

    def start(self) -> bool:
        """
        Ouvre la caméra avec un timeout de 5 secondes au total.

        Stratégie en deux tentatives :
          1. CAP_DSHOW (DirectShow, Windows) : plus rapide à initialiser sous Windows.
          2. CAP_ANY (backend par défaut, généralement MSMF) : repli si DirectShow échoue.

        Chaque tentative est exécutée dans un thread avec un timeout de 4 secondes
        pour éviter de bloquer indéfiniment l'interface si la caméra est inaccessible.

        Returns:
            bool: True si la caméra a été ouverte avec succès, False sinon.
        """
        result = [False]  # Liste mutable utilisée pour partager le résultat entre threads

        def _try_open(backend):
            """Tente d'ouvrir la caméra avec le backend spécifié (exécuté dans un thread)."""
            try:
                cap = cv2.VideoCapture(self.camera_index, backend)
                if cap.isOpened():
                    self._cap = cap     # Stockage de l'objet VideoCapture si succès
                    result[0] = True
            except Exception:
                pass  # On ignore silencieusement les erreurs d'ouverture caméra

        # ── Tentative 1 : CAP_DSHOW (DirectShow — Windows) ───────────────────
        # DirectShow est plus rapide à démarrer sous Windows que MSMF.
        t = threading.Thread(target=_try_open, args=(cv2.CAP_DSHOW,), daemon=True)
        t.start()
        t.join(timeout=4)  # On attend au maximum 4 secondes

        if not result[0]:
            # DirectShow a échoué ou est trop lent — on informe et on tente le backend par défaut
            print("[CAM] CAP_DSHOW timeout — fallback au backend par défaut")
            # ── Tentative 2 : CAP_ANY (backend MSMF sous Windows) ────────────
            t2 = threading.Thread(target=_try_open, args=(cv2.CAP_ANY,), daemon=True)
            t2.start()
            t2.join(timeout=4)

        return result[0]  # True si au moins une tentative a réussi

    def stop(self):
        """
        Ferme la caméra et libère les ressources OpenCV.
        Remet _cap à None pour indiquer que la caméra est fermée.
        Doit être appelé lorsque l'écran principal est quitté ou que l'app se ferme.
        """
        if self._cap:
            self._cap.release()  # Libère la ressource matérielle (caméra)
            self._cap = None

    @property
    def is_open(self) -> bool:
        """
        Propriété en lecture seule.
        Retourne True si la caméra est ouverte et fonctionnelle.

        Returns:
            bool: True si VideoCapture est initialisé ET signale qu'il est ouvert.
        """
        return self._cap is not None and self._cap.isOpened()

    # ── Frame ─────────────────────────────────────────────────────────────────

    def get_texture(self) -> Optional[Texture]:
        """
        Lit la frame courante depuis la caméra et la convertit en texture Kivy.

        Cette méthode est appelée à chaque tick d'horloge (environ 30 fois/seconde)
        pour mettre à jour l'aperçu caméra dans l'interface.

        Étapes de conversion :
          1. Lire une frame OpenCV (format BGR, origine en haut à gauche).
          2. Retourner l'image verticalement (Kivy place l'origine en bas à gauche).
          3. Convertir les pixels en bytes bruts.
          4. Créer une texture Kivy et y copier les données (blit_buffer).

        Returns:
            Optional[Texture]: La texture Kivy prête à être affichée,
                               ou None si la caméra est fermée ou la lecture échoue.
        """
        if not self.is_open:
            return None  # Caméra non ouverte, on ne peut pas lire

        ret, frame = self._cap.read()  # ret = succès de la lecture, frame = image numpy BGR
        if not ret:
            return None  # Lecture échouée (caméra déconnectée, fin de flux...)

        # Kivy utilise un repère avec l'origine en bas à gauche (axe Y inversé par rapport à OpenCV).
        # cv2.flip(frame, 0) effectue un retournement vertical pour corriger cet écart.
        frame = cv2.flip(frame, 0)

        # Conversion de l'image numpy en séquence d'octets bruts (nécessaire pour blit_buffer)
        buf = frame.tobytes()

        # Création d'une texture Kivy aux dimensions de la frame, en format de couleur BGR
        texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]),  # (largeur, hauteur) en pixels
            colorfmt="bgr"                           # OpenCV utilise BGR (et non RGB)
        )

        # Copie des données pixels dans la texture GPU
        texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")

        return texture  # La texture est maintenant prête à être affectée à un Image widget Kivy
