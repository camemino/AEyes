/**
 * camera.js — Gestion du flux caméra via l'API Web (getUserMedia).
 *
 * Remplace capture.py (OpenCV / cv2.VideoCapture → MediaDevices API).
 * Même interface publique : start(), stop(), isOpen, captureFrame().
 */

export class Camera {
  constructor() {
    /** @type {MediaStream|null} */
    this._stream = null;
    /** @type {HTMLVideoElement|null} */
    this._videoEl = null;
  }

  /**
   * Ouvre la caméra et attache le flux à l'élément <video>.
   * Essaie d'abord la caméra arrière (environnement), puis la caméra système par défaut.
   *
   * @param {HTMLVideoElement} videoElement
   * @returns {Promise<boolean>} true si l'ouverture a réussi
   */
  async start(videoElement) {
    this._videoEl = videoElement;

    // Tentative 1 : caméra arrière (idéale sur mobile)
    const constraints = [
      { video: { facingMode: { ideal: 'environment' } } },
      { video: true },  // fallback : première caméra disponible
    ];

    for (const c of constraints) {
      try {
        this._stream = await navigator.mediaDevices.getUserMedia(c);
        this._videoEl.srcObject = this._stream;
        await this._videoEl.play();
        return true;
      } catch (err) {
        // NotAllowedError = permission refusée → inutile de réessayer
        if (err.name === 'NotAllowedError') {
          console.error('[CAM] Permission refusée :', err.message);
          this._stream = null;
          return false;
        }
        // Autre erreur (NotFoundError, OverconstrainedError) → fallback
        console.warn('[CAM] Contrainte rejetée, fallback :', err.message);
      }
    }

    this._stream = null;
    return false;
  }

  /**
   * Arrête tous les tracks actifs et libère le flux caméra.
   * Équivalent de cap.release() dans OpenCV.
   */
  stop() {
    if (this._stream) {
      this._stream.getTracks().forEach(track => track.stop());
      this._stream = null;
    }
    if (this._videoEl) {
      this._videoEl.srcObject = null;
    }
  }

  /**
   * True si un flux caméra est actuellement actif.
   * @type {boolean}
   */
  get isOpen() {
    return this._stream !== null;
  }

  /**
   * Capture le frame courant du flux vidéo et le retourne en Data URL JPEG.
   * Équivalent de cam.read() + conversion texture dans capture.py.
   *
   * @returns {string|null} Data URL "data:image/jpeg;base64,..." ou null si indisponible
   */
  captureFrame() {
    if (!this._videoEl || !this.isOpen) return null;

    const canvas = document.createElement('canvas');
    canvas.width  = this._videoEl.videoWidth  || 640;
    canvas.height = this._videoEl.videoHeight || 480;
    canvas.getContext('2d').drawImage(this._videoEl, 0, 0);
    return canvas.toDataURL('image/jpeg', 0.85);
  }
}
