/**
 * app.js — Contrôleur principal de l'application A-Eyes (web).
 *
 * Équivalent de main_screen.py + settings_screen.py dans Kivy.
 * Coordonne les modules Camera, Speaker et VoiceListener,
 * et gère la navigation entre les deux "écrans" (sections HTML).
 *
 * Architecture :
 *   - SPA (Single Page Application) : deux sections dans index.html.
 *   - Navigation par basculement de l'attribut `hidden`.
 *   - Pas de dépendance externe — modules ES natifs uniquement.
 */

import { Camera }       from './camera.js';
import { Speaker }      from './tts.js';
import { VoiceListener } from './voice.js';

class AEyesApp {
  constructor() {
    // ── Références DOM ─────────────────────────────────────────────────────
    this._mainScreen     = document.getElementById('main-screen');
    this._settingsScreen = document.getElementById('settings-screen');
    this._videoEl        = document.getElementById('camera-view');
    this._placeholder    = document.getElementById('camera-placeholder');
    this._rateSlider     = document.getElementById('rate-slider');
    this._rateValue      = document.getElementById('rate-value');

    // ── Modules métier ─────────────────────────────────────────────────────
    this._cam   = new Camera();
    this._tts   = new Speaker();
    this._voice = new VoiceListener(cmd => this._handleCommand(cmd));

    /** @type {string|null} Data URL du dernier frame capturé (DESCRIBE ou TEXT) */
    this._lastFrame   = null;
    /** @type {Array<{role: string, content: string}>} Historique de la conversation ASK */
    this._chatHistory = [];

    // ── Branchements événements ──────────────────────────────────────────────────────────
    document.getElementById('btn-describe')
      .addEventListener('click', () => this.onDescribe());
    document.getElementById('btn-text')
      .addEventListener('click', () => this.onText());
    document.getElementById('btn-ask')
      .addEventListener('click', () => this.onAsk());
    document.getElementById('btn-repeat')
      .addEventListener('click', () => this.onRepeat());
    document.getElementById('btn-settings')
      .addEventListener('click', () => this.goToSettings());
    document.getElementById('btn-back')
      .addEventListener('click', () => this.goBack());
    this._rateSlider
      .addEventListener('input', e => this.onRateChange(Number(e.target.value)));

    // ── Démarrage ──────────────────────────────────────────────────────────
    this._enterMain();
  }

  // ── Navigation ────────────────────────────────────────────────────────────

  /**
   * Affiche l'écran principal et démarre l'écoute vocale.
   * Équivalent de MainScreen.on_enter() dans Kivy.
   */
  _enterMain() {
    this._mainScreen.hidden     = false;
    this._settingsScreen.hidden = true;
    this._tts.speak('A-Eyes ready. Say describe, text, repeat, settings or stop.');
    this._voice.startListening();
    this._startCamera();
  }

  /**
   * Prépare le départ de l'écran principal : arrête caméra et voix.
   * Équivalent de MainScreen.on_leave() dans Kivy.
   */
  _leaveMain() {
    this._stopCamera();
    this._voice.stopListening();
  }

  /** Démarre le flux caméra automatiquement. */
  async _startCamera() {
    const ok = await this._cam.start(this._videoEl);
    if (ok) {
      this._videoEl.hidden     = false;
      this._placeholder.hidden = true;
    } else {
      this._tts.speak('Camera unavailable. Please check permissions.');
    }
  }

  /**
   * Navigue vers l'écran de réglages.
   * Équivalent de MainScreen.go_to_settings() + SettingsScreen.on_enter().
   */
  goToSettings() {
    this._leaveMain();
    this._mainScreen.hidden     = true;
    this._settingsScreen.hidden = false;
    this._tts.speak('Settings screen. Use the slider to adjust the speech rate.');
  }

  /**
   * Retourne à l'écran principal depuis les réglages.
   * Équivalent de SettingsScreen.go_back() dans Kivy.
   */
  goBack() {
    this._tts.speak('Settings saved.');
    this._settingsScreen.hidden = true;
    this._enterMain();
  }

  // ── Caméra ────────────────────────────────────────────────────────────────

  /**
   * Arrête le flux caméra et restaure le placeholder.
   * Équivalent de MainScreen._stop_camera() dans Kivy.
   */
  _stopCamera() {
    if (this._cam.isOpen) {
      this._cam.stop();
      this._videoEl.hidden     = true;
      this._placeholder.hidden = false;
    }
  }

  // ── Analyse IA (DESCRIBE + TEXT) ───────────────────────────────────────────────

  /**
   * Capture un frame, l'envoie à /api/describe et vocalise la réponse.
   * Équivalent de MainScreen.on_describe() dans Kivy.
   *
   * V0 → stub retourné par le backend.
   * V1 → le backend appellera un modèle de vision (GPT-4o, etc.).
   */
  async onDescribe() {
    if (!this._cam.isOpen) {
      this._tts.speak('Please activate the camera first.');
      return;
    }

    this._tts.speak('Analysing scene...');

    const dataURL = this._cam.captureFrame();
    if (!dataURL) {
      this._tts.speak('Could not capture frame.');
      return;
    }

    this._lastFrame   = dataURL;
    this._chatHistory = [];

    try {
      // Convertit le Data URL en Blob pour l'envoi multipart
      const blob = await fetch(dataURL).then(r => r.blob());
      const form = new FormData();
      form.append('file', blob, 'frame.jpg');

      const res = await fetch('/api/describe', { method: 'POST', body: form });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const { text } = await res.json();
      this._tts.speak(text);
    } catch (err) {
      console.error('[DESCRIBE]', err);
      this._tts.speak('Analysis failed. Please check your connection.');
    }
  }
  /**
   * Capture un frame, l'envoie à /api/text et vocalise le texte détecté.
   * Feature V3 : OCR pour malvoyants (panneaux, enseignes, prix, etc.).
   */
  async onText() {
    if (!this._cam.isOpen) {
      this._tts.speak('Camera not ready.');
      return;
    }

    this._tts.speak('Reading text...');

    const dataURL = this._cam.captureFrame();
    if (!dataURL) {
      this._tts.speak('Could not capture frame.');
      return;
    }

    this._lastFrame   = dataURL;
    this._chatHistory = [];

    try {
      const blob = await fetch(dataURL).then(r => r.blob());
      const form = new FormData();
      form.append('file', blob, 'frame.jpg');

      const res = await fetch('/api/text', { method: 'POST', body: form });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const { text } = await res.json();
      this._tts.speak(text);
    } catch (err) {
      console.error('[TEXT]', err);
      this._tts.speak('Text reading failed. Please check your connection.');
    }
  }
  // ── Questions (ASK) ─────────────────────────────────────────────────────────────

  onAsk() {
    if (!this._lastFrame) {
      this._tts.speak('Please describe or read text first.');
      return;
    }
    this._tts.speak('Speak your question.');
    this._voice.captureOnce(question => {
      if (!question || !question.trim()) {
        this._tts.speak('No question detected. Please try again.');
        return;
      }
      this._sendQuestion(question.trim());
    });
  }

  async _sendQuestion(question) {
    this._tts.speak('Thinking...');
    try {
      const blob = await fetch(this._lastFrame).then(r => r.blob());
      const form = new FormData();
      form.append('file', blob, 'frame.jpg');
      form.append('question', question);
      form.append('history', JSON.stringify(this._chatHistory));

      const res = await fetch('/api/ask', { method: 'POST', body: form });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const { text } = await res.json();
      this._chatHistory.push({ role: 'user',      content: question });
      this._chatHistory.push({ role: 'assistant', content: text     });

      this._tts.speak(text);
    } catch (err) {
      console.error('[ASK]', err);
      this._tts.speak('Could not get an answer. Please try again.');
    }
  }
  // ── TTS ───────────────────────────────────────────────────────────────────

  /** Relit le dernier message. Équivalent de MainScreen.on_repeat(). */
  onRepeat() {
    this._tts.repeat();
  }

  /**
   * Met à jour la vitesse TTS et l'affichage de la valeur.
   * Équivalent de SettingsScreen.on_rate_change() dans Kivy.
   *
   * @param {number} wpm — valeur du slider (80–250)
   */
  onRateChange(wpm) {
    this._tts.setRate(wpm);
    this._rateValue.textContent = `${wpm} words/min`;
    this._rateSlider.setAttribute('aria-valuenow', String(wpm));
  }

  // ── Commandes vocales ─────────────────────────────────────────────────────

  /**
   * Dispatche une commande vocale vers l'action correspondante.
   * Équivalent de MainScreen._handle_voice_command() dans Kivy.
   *
   * @param {string} command — clé de la table COMMANDS dans voice.js
   */
  _handleCommand(command) {
    // Commande ask:<question> générée par voice.js (Option A)
    if (command.startsWith('ask:')) {
      const question = command.slice(4).trim();
      if (!this._lastFrame) {
        this._tts.speak('Please describe or read text first.');
      } else if (question) {
        this._sendQuestion(question);
      }
      return;
    }

    const actions = {
      text:     () => this.onText(),
      describe: () => this.onDescribe(),
      ask:      () => this.onAsk(),
      repeat:   () => this.onRepeat(),
      settings: () => this.goToSettings(),
      stop:     () => { this._stopCamera(); this._tts.speak('Camera off.'); },
      help:     () => this._tts.speak(
        'Available commands: describe, text, ask [question], repeat, settings, stop.'
      ),
    };
    (actions[command] ?? (() => {}))();
  }
}

// Lance l'application une fois le DOM prêt
document.addEventListener('DOMContentLoaded', () => new AEyesApp());
