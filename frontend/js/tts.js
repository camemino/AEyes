/**
 * tts.js — Synthèse vocale via l'API Web Speech Synthesis.
 *
 * Remplace speaker.py (SAPI win32com / plyer → SpeechSynthesisUtterance).
 * Même API publique : speak(text), repeat(), setRate(wpm).
 *
 * Correspondance de vitesse :
 *   pyttsx3 : vitesse en mots/minute (défaut 160, min 80, max 250)
 *   Web API  : utterance.rate — float normalisé, 1.0 = vitesse normale
 *   Formule  : webRate = wpm / 160   (160 wpm → 1.0)
 */

export class Speaker {
  constructor() {
    this._synth = window.speechSynthesis;

    /** @type {string} Dernier message prononcé (pour repeat()) */
    this._lastMessage = '';

    /** Vitesse normalisée pour l'API Web (160 wpm → 1.0) */
    this._rate = 1.0;
  }

  /**
   * Interrompt la lecture en cours et lit <text>.
   * Non-bloquant — retourne immédiatement (lecture asynchrone).
   *
   * @param {string} text
   */
  speak(text) {
    // Annule l'éventuelle lecture en cours pour éviter les files
    this._synth.cancel();
    this._lastMessage = text;

    const u = new SpeechSynthesisUtterance(text);
    u.rate = this._rate;
    u.lang = 'en-US';
    this._synth.speak(u);
  }

  /** Relit le dernier message prononcé. Équivalent de repeat() dans speaker.py. */
  repeat() {
    if (this._lastMessage) {
      this.speak(this._lastMessage);
    }
  }

  /**
   * Modifie la vitesse de parole pour les prochains messages.
   *
   * @param {number} wpm — vitesse en mots/minute (80–250, défaut 160)
   */
  setRate(wpm) {
    // Clamp entre les limites de l'API Web
    this._rate = Math.max(0.1, Math.min(10, wpm / 160));
  }
}
