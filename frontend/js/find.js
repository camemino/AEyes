/**
 * find.js — Mode FIND : recherche guidée d'un objet à la voix.
 *
 * Deux classes :
 *   - Beeper       : 2 sons mono (found / lost) via Web Audio API.
 *   - FindSession  : boucle d'analyse — POST /api/find, TTS conditionnel, bips.
 *
 * Aucune dépendance externe. Compatible iOS Safari moyennant un geste
 * utilisateur préalable (initialisé par app.js).
 */

/* ─────────────────────────────────────────────────────────────────────────
   Configuration
   ──────────────────────────────────────────────────────────────────────── */

/** Durée maximale d'une session FIND avant timeout. */
const FIND_TIMEOUT_MS = 30_000;

/** Largeur cible du frame envoyé (réduit latence + tokens). */
const FRAME_WIDTH = 512;

/** Qualité JPEG du frame envoyé. */
const FRAME_QUALITY = 0.7;


/* ─────────────────────────────────────────────────────────────────────────
   Beeper — 2 sons mono : aigu pour "found", grave pour "lost".
   ──────────────────────────────────────────────────────────────────────── */

export class Beeper {
  constructor() {
    /** @type {AudioContext|null} */
    this._ctx = null;
  }

  /**
   * Initialise (ou réutilise) un AudioContext.
   * Doit être appelé depuis un handler d'événement utilisateur (iOS Safari).
   */
  init() {
    if (this._ctx) return;
    const Ctor = window.AudioContext || window.webkitAudioContext;
    if (!Ctor) {
      console.warn('[BEEPER] Web Audio API indisponible.');
      return;
    }
    this._ctx = new Ctor();
  }

  /** Reprend le contexte si suspendu (iOS Safari après inactivité). */
  async resume() {
    if (this._ctx?.state === 'suspended') {
      try { await this._ctx.resume(); } catch (_) { /* noop */ }
    }
  }

  /**
   * Joue un oscillateur sinus avec rampe linéaire de fréquence + enveloppe.
   * @param {number} freqStart Hz
   * @param {number} freqEnd   Hz
   * @param {number} durationMs
   */
  _tone(freqStart, freqEnd, durationMs) {
    if (!this._ctx) return;
    const t0 = this._ctx.currentTime;
    const dur = durationMs / 1000;

    const osc  = this._ctx.createOscillator();
    const gain = this._ctx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(freqStart, t0);
    osc.frequency.linearRampToValueAtTime(freqEnd, t0 + dur);

    // Enveloppe : attaque 20 ms, sustain, release 80 ms — évite les clics.
    gain.gain.setValueAtTime(0, t0);
    gain.gain.linearRampToValueAtTime(0.4, t0 + 0.02);
    gain.gain.setValueAtTime(0.4, t0 + Math.max(0.02, dur - 0.08));
    gain.gain.linearRampToValueAtTime(0, t0 + dur);

    osc.connect(gain).connect(this._ctx.destination);
    osc.start(t0);
    osc.stop(t0 + dur + 0.02);
  }

  /** Double chirp ascendant — succès. */
  beepFound() {
    this._tone(800, 1200, 140);
    setTimeout(() => this._tone(900, 1400, 160), 150);
  }

  /** Ton grave bref — perdu / hors champ. */
  beepLost() {
    this._tone(220, 180, 220);
  }

  /** Bip neutre très court — indique que l'analyse commence ("photo prise"). */
  beepScan() {
    this._tone(480, 480, 60);
  }
}


/* ─────────────────────────────────────────────────────────────────────────
   Utilitaires frame : downscale à FRAME_WIDTH avant POST.
   ──────────────────────────────────────────────────────────────────────── */

/**
 * Downscale d'un data URL JPEG vers un Blob plus léger.
 * @param {string} dataURL
 * @returns {Promise<Blob>}
 */
async function _downscale(dataURL) {
  const img = await new Promise((resolve, reject) => {
    const i = new Image();
    i.onload = () => resolve(i);
    i.onerror = reject;
    i.src = dataURL;
  });

  const ratio = Math.min(1, FRAME_WIDTH / img.width);
  const w = Math.round(img.width  * ratio);
  const h = Math.round(img.height * ratio);

  const canvas = document.createElement('canvas');
  canvas.width  = w;
  canvas.height = h;
  canvas.getContext('2d').drawImage(img, 0, 0, w, h);

  return new Promise(resolve => {
    canvas.toBlob(b => resolve(b), 'image/jpeg', FRAME_QUALITY);
  });
}


/* ─────────────────────────────────────────────────────────────────────────
   FindSession — orchestrateur de la boucle de guidage.
   ──────────────────────────────────────────────────────────────────────── */

export class FindSession {
  /**
   * @param {object} deps
   * @param {import('./camera.js').Camera}  deps.cam
   * @param {import('./tts.js').Speaker}    deps.tts
   * @param {Beeper}                        deps.beeper
   * @param {string}                        deps.target
   * @param {() => void}                    deps.onDone   Appelé en fin de session (toutes raisons).
   */
  constructor({ cam, tts, beeper, target, onDone, onAnalysing = () => {} }) {
    this._cam         = cam;
    this._tts         = tts;
    this._beeper      = beeper;
    this._target      = target;
    this._onDone      = onDone;
    this._onAnalysing = onAnalysing;

    this._cancelled  = false;
    this._lastSpoken = null;
    this._startedAt  = Date.now();

    this._beeper.resume();
    this._tts.speak(`Looking for ${target}.`, () => this._loop());
  }

  /** Demande l'arrêt de la session (commande vocale "stop" ou bouton STOP). */
  cancel() {
    if (this._cancelled) return;
    this._cancelled = true;
    this._tts.cancel();
    this._tts.speak('Search cancelled.', () => this._onDone());
  }

  /** Boucle principale — une itération = capture + POST + TTS conditionnel. */
  async _loop() {
    while (!this._cancelled) {
      if (Date.now() - this._startedAt > FIND_TIMEOUT_MS) {
        this._tts.speak('I cannot find it.', () => this._onDone());
        return;
      }

      const dataURL = this._cam.captureFrame();
      if (!dataURL) {
        this._tts.speak('Camera error.', () => this._onDone());
        return;
      }

      let result;
      try {
        const blob = await _downscale(dataURL);
        const form = new FormData();
        form.append('file', blob, 'frame.jpg');
        form.append('target', this._target);

        this._beeper.beepScan();
        this._onAnalysing(true);
        const res = await fetch('/api/find', { method: 'POST', body: form });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        result = await res.json();
        this._onAnalysing(false);
      } catch (err) {
        this._onAnalysing(false);
        console.error('[FIND]', err);
        this._tts.speak('Connection lost.', () => this._onDone());
        return;
      }

      if (this._cancelled) return;

      const { direction, distance, text } = result;

      // Succès : bip + TTS "Found it" + sortie.
      if (direction === 'found' && distance !== 'far') {
        this._beeper.beepFound();
        this._tts.speak('Found it!', () => this._onDone());
        return;
      }

      // Hors champ : bip grave.
      if (direction === 'not_visible') {
        this._beeper.beepLost();
      }

      // TTS seulement si la phrase change — silence quand l'utilisateur est OK.
      if (text && text !== this._lastSpoken) {
        this._lastSpoken = text;
        await this._speakAndWait(text);
      } else {
        // Petit délai pour ne pas marteler /api/find à pleine vitesse.
        await new Promise(r => setTimeout(r, 400));
      }
    }
  }

  /**
   * Parle puis attend la fin de l'utterance.
   * @param {string} text
   * @returns {Promise<void>}
   */
  _speakAndWait(text) {
    return new Promise(resolve => this._tts.speak(text, resolve));
  }
}
