/**
 * Quizmondo Retro Web Audio API Synthesizer
 * Provides 100% dependency-free synthesized sound effects for:
 * - Climber ascents, slips, shields, and summits
 * - Vault Spinner mechanical clicks and jackpots
 * - Hero TV carousel CRT blips
 */
(function(window) {
  'use strict';

  var AudioCtx = window.AudioContext || window.webkitAudioContext;
  var ctx = null;
  var isMuted = localStorage.getItem('qm_sfx_muted') === '1';

  function getContext() {
    if (!ctx && AudioCtx) {
      try {
        ctx = new AudioCtx();
      } catch (e) {
        console.warn('Web Audio API not supported', e);
      }
    }
    if (ctx && ctx.state === 'suspended') {
      ctx.resume().catch(function() {});
    }
    return ctx;
  }

  // Pre-unlock on first user interaction
  function unlock() {
    getContext();
    document.removeEventListener('click', unlock);
    document.removeEventListener('keydown', unlock);
    document.removeEventListener('touchstart', unlock);
  }
  document.addEventListener('click', unlock, { once: true, passive: true });
  document.addEventListener('keydown', unlock, { once: true, passive: true });
  document.addEventListener('touchstart', unlock, { once: true, passive: true });

  var sounds = {
    // Mechanical peg tick on lucky wheel or step movement
    tick: function(c) {
      var osc = c.createOscillator();
      var gain = c.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(520, c.currentTime);
      osc.frequency.exponentialRampToValueAtTime(140, c.currentTime + 0.035);
      gain.gain.setValueAtTime(0.18, c.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, c.currentTime + 0.035);
      osc.connect(gain);
      gain.connect(c.destination);
      osc.start(c.currentTime);
      osc.stop(c.currentTime + 0.04);
    },

    // Climber rope pull / step ascend
    pull: function(c) {
      var osc = c.createOscillator();
      var gain = c.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(280, c.currentTime);
      osc.frequency.exponentialRampToValueAtTime(560, c.currentTime + 0.12);
      gain.gain.setValueAtTime(0.2, c.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, c.currentTime + 0.14);
      osc.connect(gain);
      gain.connect(c.destination);
      osc.start(c.currentTime);
      osc.stop(c.currentTime + 0.15);
    },

    // Slip / fall down the wall
    slip: function(c) {
      var osc = c.createOscillator();
      var gain = c.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(450, c.currentTime);
      osc.frequency.exponentialRampToValueAtTime(90, c.currentTime + 0.38);
      gain.gain.setValueAtTime(0.25, c.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, c.currentTime + 0.4);
      osc.connect(gain);
      gain.connect(c.destination);
      osc.start(c.currentTime);
      osc.stop(c.currentTime + 0.42);
    },

    // Shield deflect
    shield: function(c) {
      var osc = c.createOscillator();
      var gain = c.createGain();
      osc.type = 'square';
      osc.frequency.setValueAtTime(620, c.currentTime);
      osc.frequency.exponentialRampToValueAtTime(880, c.currentTime + 0.08);
      osc.frequency.exponentialRampToValueAtTime(1200, c.currentTime + 0.2);
      gain.gain.setValueAtTime(0.15, c.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, c.currentTime + 0.25);
      osc.connect(gain);
      gain.connect(c.destination);
      osc.start(c.currentTime);
      osc.stop(c.currentTime + 0.26);
    },

    // Bank coins safely (metallic register chime)
    bank: function(c) {
      [988, 1318].forEach(function(freq, i) {
        var osc = c.createOscillator();
        var gain = c.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, c.currentTime + i * 0.08);
        gain.gain.setValueAtTime(0.22, c.currentTime + i * 0.08);
        gain.gain.exponentialRampToValueAtTime(0.001, c.currentTime + i * 0.08 + 0.28);
        osc.connect(gain);
        gain.connect(c.destination);
        osc.start(c.currentTime + i * 0.08);
        osc.stop(c.currentTime + i * 0.08 + 0.3);
      });
    },

    // Jackpot / Summit triumphant fanfare
    fanfare: function(c) {
      var notes = [523.25, 659.25, 783.99, 1046.50];
      notes.forEach(function(freq, idx) {
        var osc = c.createOscillator();
        var gain = c.createGain();
        var t = c.currentTime + idx * 0.11;
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, t);
        gain.gain.setValueAtTime(0.2, t);
        gain.gain.exponentialRampToValueAtTime(0.001, t + (idx === notes.length - 1 ? 0.45 : 0.18));
        osc.connect(gain);
        gain.connect(c.destination);
        osc.start(t);
        osc.stop(t + 0.5);
      });
    },

    // Hero CRT TV blip
    blip: function(c) {
      var osc = c.createOscillator();
      var gain = c.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(700, c.currentTime);
      osc.frequency.exponentialRampToValueAtTime(950, c.currentTime + 0.04);
      gain.gain.setValueAtTime(0.08, c.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, c.currentTime + 0.05);
      osc.connect(gain);
      gain.connect(c.destination);
      osc.start(c.currentTime);
      osc.stop(c.currentTime + 0.06);
    }
  };

  function playSound(type) {
    if (isMuted) return;
    var c = getContext();
    if (!c) return;
    if (sounds[type]) {
      try {
        sounds[type](c);
      } catch (err) {
        console.warn('Sound play error:', err);
      }
    }
  }

  function toggleMute() {
    isMuted = !isMuted;
    localStorage.setItem('qm_sfx_muted', isMuted ? '1' : '0');
    updateMuteUI();
    if (!isMuted) {
      playSound('blip');
    }
    return isMuted;
  }

  function updateMuteUI() {
    var btns = document.querySelectorAll('[data-qm-sound-toggle]');
    btns.forEach(function(btn) {
      btn.innerHTML = isMuted ? '🔇 <span class="hidden sm:inline">SFX OFF</span>' : '🔊 <span class="hidden sm:inline">SFX ON</span>';
      btn.setAttribute('aria-pressed', isMuted ? 'false' : 'true');
    });
  }

  document.addEventListener('DOMContentLoaded', updateMuteUI);

  // Global exports
  window.qmPlaySound = playSound;
  window.qmToggleMute = toggleMute;
  window.qmIsMuted = function() { return isMuted; };

})(window);
