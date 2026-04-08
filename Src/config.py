"""
config.py — Constantes globales de configuration de l'application A-Eyes.

Ce fichier centralise toutes les valeurs paramétrables de l'application :
couleurs de l'interface, tailles de police, dimensions des boutons,
paramètres de synthèse vocale (TTS) et de la caméra.
Modifier ces valeurs ici suffit pour adapter l'apparence et le comportement
de l'application sans toucher au code fonctionnel.
"""

# ── Couleurs (fort contraste pour malvoyants) ─────────────────────────────────
# Les couleurs sont exprimées en format RGBA normalisé (valeurs entre 0.0 et 1.0).
# Le fort contraste est essentiel pour les utilisateurs malvoyants.
BG_COLOR        = (0, 0, 0, 1)          # Fond de l'écran : noir pur
BTN_SCAN_COLOR  = (1, 0.8, 0, 1)        # Bouton SCAN : jaune vif (très visible)
BTN_DESC_COLOR  = (0.1, 0.7, 0.3, 1)   # Bouton DÉCRIRE : vert
BTN_REP_COLOR   = (0.2, 0.6, 1, 1)     # Bouton RÉPÉTER : bleu
BTN_SET_COLOR   = (0.3, 0.3, 0.3, 1)   # Bouton RÉGLAGES : gris neutre
BTN_DARK_TEXT   = (0, 0, 0, 1)         # Texte noir — utilisé sur fond jaune (contraste élevé)
BTN_LIGHT_TEXT  = (1, 1, 1, 1)         # Texte blanc — utilisé sur fond bleu, vert ou gris

# ── Typographie ───────────────────────────────────────────────────────────────
# Les tailles sont exprimées en "sp" (scale-independent pixels) : elles s'adaptent
# automatiquement à la taille de l'écran et aux préférences d'accessibilité du système.
FONT_SIZE_XL = "36sp"   # Très grande police — titres principaux
FONT_SIZE_L  = "32sp"   # Grande police — boutons principaux
FONT_SIZE_M  = "26sp"   # Police moyenne — contenu courant
FONT_SIZE_S  = "22sp"   # Petite police — éléments secondaires

# ── Tailles boutons ───────────────────────────────────────────────────────────
# Les tailles sont exprimées en "dp" (density-independent pixels) : elles restent
# cohérentes sur des écrans de densités différentes (smartphone, tablette...).
# Des boutons grands facilitent l'utilisation pour les malvoyants.
BTN_HEIGHT_XL = "110dp"  # Hauteur maximale — bouton prioritaire (ex: SCAN)
BTN_HEIGHT_L  = "95dp"   # Hauteur grande
BTN_HEIGHT_M  = "80dp"   # Hauteur standard
BTN_HEIGHT_S  = "65dp"   # Hauteur réduite — boutons secondaires
PADDING       = "18dp"   # Marge intérieure des conteneurs (espace autour du contenu)
SPACING       = "12dp"   # Espacement entre les widgets dans un layout

# ── TTS (Text-To-Speech / Synthèse vocale) ───────────────────────────────────
# Paramètres de la synthèse vocale utilisée pour lire les messages à l'utilisateur.
TTS_RATE_DEFAULT = 160   # Vitesse par défaut en mots/minute (valeur confortable)
TTS_RATE_MIN     = 80    # Vitesse minimale autorisée dans les réglages
TTS_RATE_MAX     = 250   # Vitesse maximale autorisée dans les réglages
TTS_LANG         = "en"  # Langue de la synthèse vocale (anglais)

# ── Caméra ────────────────────────────────────────────────────────────────────
CAMERA_FPS    = 30        # Nombre d'images par seconde demandé au flux caméra
CAMERA_INDEX  = 0         # Indice de la caméra à utiliser (0 = caméra principale du système)

# ── Message de substitution DÉCRIRE (V0 — IA non connectée) ──────────────────
# En version 0, la fonction d'analyse de scène par IA n'est pas encore implémentée.
# Ce message est lu à la place lorsque l'utilisateur appuie sur "DÉCRIRE".
DESCRIBE_STUB_MSG = "Analysis in progress... feature available in version 1."
