/**
 * voice.js — Reconnaissance vocale continue via l'API Web Speech Recognition.
 *
 * Remplace listener.py (SpeechRecognition + Google STT → Web Speech API).
 * Même logique : table COMMANDS identique, auto-restart, graceful degradation.
 *
 * Dégradation gracieuse : si le navigateur ne supporte pas l'API (ex: Firefox),
 * `available` est false et aucune erreur n'est levée. L'app reste fonctionnelle
 * via les boutons de l'interface.
 */

/**
 * Table des commandes reconnues — identique à COMMANDS dans listener.py.
 * Mot-clé détecté dans la transcription → identifiant de commande transmis au callback.
 * @type {Record<string, string>}
 */
const COMMANDS = {
  text:     'text',
  describe: 'describe',
  repeat:   'repeat',
  settings: 'settings',
  help:     'help',
  stop:     'stop',
};

export class VoiceListener {
  /**
   * @param {(command: string) => void} onCommand
   *   Callback appelé avec l'identifiant de commande détecté.
   */
  constructor(onCommand) {
    this._onCommand      = onCommand;
    this._active         = false;
    this._recognition    = null;
    this._captureCallback = null;

    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    /** @type {boolean} False si le navigateur ne supporte pas l'API */
    this.available = !!SpeechRecognition;

    if (!this.available) {
      console.warn('[VOICE] SpeechRecognition non supportée sur ce navigateur.');
      return;
    }

    this._recognition = new SpeechRecognition();
    this._recognition.continuous      = true;   // écoute continue
    this._recognition.interimResults  = false;  // résultats finaux uniquement
    this._recognition.lang            = 'en-US';

    this._recognition.onresult = e => this._handleResult(e);

    this._recognition.onerror = e => {
      // 'no-speech' est normal (silence) — ne pas loguer
      if (e.error !== 'no-speech') {
        console.warn('[VOICE] Erreur :', e.error);
      }
    };

    // Auto-restart : si la session se termine (timeout navigateur), relance
    this._recognition.onend = () => {
      if (this._active) {
        this._recognition.start();
      }
    };
  }

  /** Démarre l'écoute continue du microphone. */
  startListening() {
    if (!this.available || this._active) return;
    this._active = true;
    this._recognition.start();
  }

  /** Arrête l'écoute et libère le microphone. */
  stopListening() {
    if (!this.available) return;
    this._active = false;
    this._recognition.stop();
  }

  /**
   * Traite un résultat de reconnaissance et déclenche le callback si un mot-clé correspond.
   * @param {SpeechRecognitionEvent} event
   */
  /**
   * Capture la prochaine transcription vocale comme texte libre (mode question).
   * @param {(transcript: string) => void} callback
   */
  captureOnce(callback) {
    this._captureCallback = callback;
  }

  _handleResult(event) {
    const lastResult = event.results[event.results.length - 1];
    const transcript = lastResult[0].transcript.trim();

    // Mode capture (bouton ASK) : la prochaine phrase est la question
    if (this._captureCallback) {
      const cb = this._captureCallback;
      this._captureCallback = null;
      cb(transcript);
      return;
    }

    const lower = transcript.toLowerCase();

    // Option A : "ask <question>" en une seule phrase
    const askIdx = lower.indexOf('ask ');
    if (askIdx !== -1) {
      const question = transcript.slice(askIdx + 4).trim();
      if (question) {
        this._onCommand('ask:' + question);
        return;
      }
    }

    for (const [keyword, command] of Object.entries(COMMANDS)) {
      if (lower.includes(keyword)) {
        this._onCommand(command);
        return;
      }
    }
  }
}
