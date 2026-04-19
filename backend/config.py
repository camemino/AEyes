# config.py — Constantes partagées entre le backend et (via CSS vars) le frontend.

# ── TTS (Text-To-Speech) ──────────────────────────────────────────────────────
TTS_RATE_DEFAULT = 160   # Vitesse par défaut en mots/minute
TTS_RATE_MIN     = 80    # Vitesse minimale autorisée
TTS_RATE_MAX     = 250   # Vitesse maximale autorisée
TTS_LANG         = "en"  # Langue de la synthèse vocale

# ── Message stub DÉCRIRE (V0 — IA non connectée) ─────────────────────────────
# Remplacé en V1 par un appel à un modèle de vision (GPT-4o, Gemini Vision, etc.)
DESCRIBE_STUB_MSG = "Analysis in progress... feature available in version 1."
