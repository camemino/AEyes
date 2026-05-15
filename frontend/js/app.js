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
import { Beeper, FindSession } from './find.js';

class AEyesApp {
  constructor() {
    // ── Références DOM ─────────────────────────────────────────────────────
    this._mainScreen  = document.getElementById('main-screen');
    this._videoEl     = document.getElementById('camera-view');

    // ── Modules métier ─────────────────────────────────────────────────────
    this._cam    = new Camera();
    this._tts    = new Speaker();
    this._beeper = new Beeper();
    this._voice  = new VoiceListener(cmd => this._handleCommand(cmd));

    /** @type {string|null} Data URL du dernier frame capturé (DESCRIBE ou TEXT) */
    this._lastFrame   = null;
    /** @type {Array<{role: string, content: string}>} Historique de la conversation ASK */
    this._chatHistory = [];
    /** @type {FindSession|null} Session FIND en cours, sinon null */
    this._findSession = null;

    // ── Overlay STOP (mode FIND) ───────────────────────────────────────────
    this._findOverlay   = document.getElementById('find-overlay');
    this._findTargetEl  = document.getElementById('find-target');
    this._findStatusEl  = document.getElementById('find-status');
    document.getElementById('btn-find-stop')
      ?.addEventListener('click', () => this._findSession?.cancel());

    // ── Init AudioContext au premier geste utilisateur (iOS Safari) ────────
    const initAudio = () => {
      this._beeper.init();
      document.removeEventListener('pointerdown', initAudio);
    };
    document.addEventListener('pointerdown', initAudio, { once: true });

    /** Boutons d'action — désactivés pendant tout traitement */
    this._actionBtns = [
      document.getElementById('btn-describe'),
      document.getElementById('btn-text'),
      document.getElementById('btn-details'),
      document.getElementById('btn-ask'),
      document.getElementById('btn-find'),
    ];

    // ── Branchements événements ──────────────────────────────────────────────────────────
    document.getElementById('btn-describe')
      .addEventListener('click', () => this.onDescribe());
    document.getElementById('btn-text')
      .addEventListener('click', () => this.onText());
    document.getElementById('btn-details')
      .addEventListener('click', () => this.onDetails());
    document.getElementById('btn-ask')
      .addEventListener('click', () => this.onAsk());
    document.getElementById('btn-find')
      .addEventListener('click', () => this.onFindPrompt());
    document.getElementById('btn-repeat')
      .addEventListener('click', () => this.onRepeat());

    // ── Démarrage ──────────────────────────────────────────────────────────
    this._enterMain();
  }

  // ── État occupé / libre ─────────────────────────────────────────────

  /** Désactive les boutons d'action + arrête la reconnaissance vocale + vibration courte. */
  _setBusy() {
    this._actionBtns.forEach(b => { b.disabled = true; });
    this._voice.stopListening();
    navigator.vibrate?.(80);
  }

  /** Réactive les boutons d'action + redémarre la reconnaissance vocale + double vibration. */
  _setIdle() {
    this._actionBtns.forEach(b => { b.disabled = false; });
    this._voice.startListening();
    navigator.vibrate?.([80, 60, 80]);
  }

  // ── Navigation ────────────────────────────────────────────────────────────

  /**
   * Affiche l'écran principal et démarre l'écoute vocale.
   * Équivalent de MainScreen.on_enter() dans Kivy.
   */
  _enterMain() {
    this._mainScreen.hidden = false;
    this._startCamera();
    // Démarre l'écoute vocale seulement après le message d'accueil,
    // pour éviter que le TTS soit capté par le micro.
    this._tts.speak(
      'A-Eyes ready. Say describe, text, details, repeat or stop.',
      () => this._voice.startListening()
    );
  }

  /** Démarre le flux caméra automatiquement. */
  async _startCamera() {
    const ok = await this._cam.start(this._videoEl);
    if (!ok) {
      this._tts.speak('Camera unavailable. Please check permissions.');
    }
  }

  // ── Caméra ────────────────────────────────────────────────────────────────

  /**
   * Arrête le flux caméra et restaure le placeholder.
   * Équivalent de MainScreen._stop_camera() dans Kivy.
   */
  _stopCamera() {
    if (this._cam.isOpen) {
      this._cam.stop();
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

    this._setBusy();
    this._tts.speak('Analysing scene...');

    const dataURL = this._cam.captureFrame();
    if (!dataURL) {
      this._tts.speak('Could not capture frame.', () => this._setIdle());
      return;
    }

    this._lastFrame   = dataURL;
    this._chatHistory = [];

    try {
      const blob = await fetch(dataURL).then(r => r.blob());
      const form = new FormData();
      form.append('file', blob, 'frame.jpg');

      const res = await fetch('/api/describe', { method: 'POST', body: form });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const { text } = await res.json();
      this._tts.speak(text, () => this._setIdle());
    } catch (err) {
      console.error('[DESCRIBE]', err);
      this._tts.speak('Analysis failed. Please check your connection.', () => this._setIdle());
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

    this._setBusy();
    this._tts.speak('Reading text...');

    const dataURL = this._cam.captureFrame();
    if (!dataURL) {
      this._tts.speak('Could not capture frame.', () => this._setIdle());
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
      this._tts.speak(text, () => this._setIdle());
    } catch (err) {
      console.error('[TEXT]', err);
      this._tts.speak('Text reading failed. Please check your connection.', () => this._setIdle());
    }
  }
  /**
   * Envoie _lastFrame à /api/details et vocalise la description détaillée.
   * Utilise la dernière image capturée par DESCRIBE ou TEXT — pas de nouvelle capture.
   */
  async onDetails() {
    if (!this._lastFrame) {
      this._tts.speak('Please describe or read text first.');
      return;
    }

    this._setBusy();
    this._tts.speak('Analysing in detail...');

    try {
      const blob = await fetch(this._lastFrame).then(r => r.blob());
      const form = new FormData();
      form.append('file', blob, 'frame.jpg');

      const res = await fetch('/api/details', { method: 'POST', body: form });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const { text } = await res.json();
      this._tts.speak(text, () => this._setIdle());
    } catch (err) {
      console.error('[DETAILS]', err);
      this._tts.speak('Analysis failed. Please check your connection.', () => this._setIdle());
    }
  }

  // ── Questions (ASK) ─────────────────────────────────────────────────────────────

  onAsk() {
    if (!this._lastFrame) {
      this._tts.speak('Please describe or read text first.');
      return;
    }
    // Stop listening pendant le TTS "Speak your question.",
    // puis redémarre pour capturer la question de l'utilisateur.
    this._voice.stopListening();
    this._tts.speak('Speak your question.', () => {
      this._voice.startListening();
      this._voice.captureOnce(question => {
        this._voice.stopListening();
        if (!question || !question.trim()) {
          this._tts.speak('No question detected. Please try again.', () => this._setIdle());
          return;
        }
        this._sendQuestion(question.trim());
      });
    });
  }

  async _sendQuestion(question) {
    this._setBusy();
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

      this._tts.speak(text, () => this._setIdle());
    } catch (err) {
      console.error('[ASK]', err);
      this._tts.speak('Could not get an answer. Please try again.', () => this._setIdle());
    }
  }

  // ── FIND ──────────────────────────────────────────────────────────────────

  /**
   * Déclenché par le bouton FIND : demande vocalement l'objet à chercher,
   * puis lance onFind(target). Même mécanique que onAsk().
   */
  onFindPrompt() {
    if (!this._cam.isOpen) {
      this._tts.speak('Camera not ready.');
      return;
    }
    if (this._findSession) return;

    this._voice.stopListening();
    this._tts.speak('What are you looking for?', () => {
      this._voice.startListening();
      this._voice.captureOnce(target => {
        this._voice.stopListening();
        if (!target || !target.trim()) {
          this._tts.speak('No target heard. Please try again.', () => this._setIdle());
          return;
        }
        this.onFind(target.trim());
      });
    });
  }

  /**
   * Démarre une session de recherche guidée pour <target>.
   * Lancée depuis la commande vocale "find <target>" ou depuis onFindPrompt().
   * @param {string} target
   */
  onFind(target) {
    if (!this._cam.isOpen) {
      this._tts.speak('Camera not ready.');
      return;
    }
    if (this._findSession) return;

    this._setBusy();

    // Overlay STOP plein écran
    if (this._findOverlay) {
      this._findTargetEl.textContent = target;
      this._findOverlay.hidden = false;
    }

    this._findSession = new FindSession({
      cam:    this._cam,
      tts:    this._tts,
      beeper: this._beeper,
      target,
      onAnalysing: (busy) => {
        if (this._findStatusEl) this._findStatusEl.hidden = !busy;
      },
      onDone: () => {
        this._findSession = null;
        if (this._findOverlay)  this._findOverlay.hidden = true;
        if (this._findStatusEl) this._findStatusEl.hidden = true;
        this._setIdle();
      },
    });

    // Réactive la reconnaissance vocale pour capter "stop" pendant la session.
    this._voice.startListening();
  }

  // ── TTS ───────────────────────────────────────────────────────────────────

  /** Relit le dernier message. Équivalent de MainScreen.on_repeat(). */
  onRepeat() {
    this._voice.stopListening();
    this._tts.repeat(() => this._voice.startListening());
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

    // Commande find:<target>
    if (command.startsWith('find:')) {
      const target = command.slice(5).trim();
      if (target) this.onFind(target);
      return;
    }

    // Pendant une session FIND, seul "stop" est utile
    if (this._findSession) {
      if (command === 'stop') this._findSession.cancel();
      return;
    }

    const actions = {
      text:     () => this.onText(),
      describe: () => this.onDescribe(),
      details:  () => this.onDetails(),
      ask:      () => this.onAsk(),
      repeat:   () => this.onRepeat(),
      stop: () => { this._tts.cancel(); this._setIdle(); },
      help: () => {
        this._voice.stopListening();
        this._tts.speak(
          'Available commands: describe, text, details, ask, repeat, stop.',
          () => this._voice.startListening()
        );
      },
    };
    (actions[command] ?? (() => {}))();
  }
}

// Lance l'application une fois le DOM prêt
document.addEventListener('DOMContentLoaded', () => new AEyesApp());
