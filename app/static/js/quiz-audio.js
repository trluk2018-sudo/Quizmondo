/**
 * Quizmondo Synthesized Web Audio API Sound Engine.
 * Zero-bandwidth audio synthesis: generates all arcade sounds procedurally without downloading MP3s.
 */
class QuizAudioEngine {
  constructor() {
    this.ctx = null;
    this.isMuted = localStorage.getItem('qm_audio_muted') === 'true';
  }

  _init() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) {
        this.ctx = new AudioCtx();
      }
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  toggleMute() {
    this.isMuted = !this.isMuted;
    localStorage.setItem('qm_audio_muted', this.isMuted);
    return this.isMuted;
  }

  playTick() {
    if (this.isMuted) return;
    this._init();
    if (!this.ctx) return;

    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(800, this.ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(300, this.ctx.currentTime + 0.04);
    gain.gain.setValueAtTime(0.08, this.ctx.currentTime);
    gain.gain.linearRampToValueAtTime(0.001, this.ctx.currentTime + 0.04);

    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start();
    osc.stop(this.ctx.currentTime + 0.05);
  }

  playHeartbeat() {
    if (this.isMuted) return;
    this._init();
    if (!this.ctx) return;

    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(75, this.ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(40, this.ctx.currentTime + 0.12);
    gain.gain.setValueAtTime(0.2, this.ctx.currentTime);
    gain.gain.linearRampToValueAtTime(0.001, this.ctx.currentTime + 0.15);

    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start();
    osc.stop(this.ctx.currentTime + 0.16);
  }

  playCorrect() {
    if (this.isMuted) return;
    this._init();
    if (!this.ctx) return;

    const now = this.ctx.currentTime;
    // Ascending arpeggio C5 (523Hz) -> E5 (659Hz) -> G5 (784Hz) -> C6 (1046Hz)
    const notes = [523.25, 659.25, 783.99, 1046.50];
    notes.forEach((freq, idx) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, now + idx * 0.06);

      gain.gain.setValueAtTime(0, now + idx * 0.06);
      gain.gain.linearRampToValueAtTime(0.12, now + idx * 0.06 + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.06 + 0.22);

      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now + idx * 0.06);
      osc.stop(now + idx * 0.06 + 0.24);
    });
  }

  playWrong() {
    if (this.isMuted) return;
    this._init();
    if (!this.ctx) return;

    const now = this.ctx.currentTime;
    const osc1 = this.ctx.createOscillator();
    const osc2 = this.ctx.createOscillator();
    const gain = this.ctx.createGain();

    osc1.type = 'sawtooth';
    osc2.type = 'triangle';
    osc1.frequency.setValueAtTime(140, now);
    osc1.frequency.linearRampToValueAtTime(90, now + 0.28);
    osc2.frequency.setValueAtTime(145, now);
    osc2.frequency.linearRampToValueAtTime(95, now + 0.28);

    gain.gain.setValueAtTime(0.12, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);

    osc1.connect(gain);
    osc2.connect(gain);
    gain.connect(this.ctx.destination);

    osc1.start(now);
    osc2.start(now);
    osc1.stop(now + 0.32);
    osc2.stop(now + 0.32);
  }

  playTurnSwitch() {
    if (this.isMuted) return;
    this._init();
    if (!this.ctx) return;

    const now = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(220, now);
    osc.frequency.exponentialRampToValueAtTime(880, now + 0.18);
    gain.gain.setValueAtTime(0.01, now);
    gain.gain.linearRampToValueAtTime(0.1, now + 0.08);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.2);

    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start(now);
    osc.stop(now + 0.22);
  }

  playVictory() {
    if (this.isMuted) return;
    this._init();
    if (!this.ctx) return;

    const now = this.ctx.currentTime;
    const notes = [
      { f: 523.25, t: 0.0 },
      { f: 659.25, t: 0.12 },
      { f: 783.99, t: 0.24 },
      { f: 1046.50, t: 0.36 },
      { f: 1318.51, t: 0.54 }
    ];
    notes.forEach((n) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(n.f, now + n.t);
      gain.gain.setValueAtTime(0.15, now + n.t);
      gain.gain.exponentialRampToValueAtTime(0.001, now + n.t + 0.35);

      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now + n.t);
      osc.stop(now + n.t + 0.38);
    });
  }
}

window.quizAudio = new QuizAudioEngine();
