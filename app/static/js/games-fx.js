/**
 * Quizmondo mini games: shared HUD, effects and score plumbing.
 *
 * Every mini game page loads this once and then only has to worry about its own
 * rules. It drives the score/time/best HUD, the streak pill, score pops,
 * confetti, the game-over overlay and posting the final score to the server.
 * Sound rides on the Arena's existing window.quizAudio engine.
 */
window.QMG = (function () {
  var gameKey = '';
  var score = 0;
  var best = 0;
  var combo = 0;
  var bestCombo = 0;
  var timerId = null;
  var timerEnd = 0;
  var timerTotal = 0;
  var onTimeout = null;
  var replayFn = null;
  var submitted = false;

  function $(id) { return document.getElementById(id); }

  // --- audio -------------------------------------------------------------
  var audio = {
    call: function (name) {
      try {
        if (window.quizAudio && typeof window.quizAudio[name] === 'function') {
          window.quizAudio[name]();
        }
      } catch (e) { /* audio is a nicety, never a blocker */ }
    },
    correct: function () { this.call('playCorrect'); },
    wrong: function () { this.call('playWrong'); },
    tick: function () { this.call('playTick'); },
    switchTurn: function () { this.call('playTurnSwitch'); },
    victory: function () { this.call('playVictory'); },
    heartbeat: function () { this.call('playHeartbeat'); },
    // A short synthesized blip at an arbitrary pitch, for pads and streaks.
    tone: function (freq, ms, type) {
      try {
        var eng = window.quizAudio;
        if (!eng || eng.isMuted) return;
        if (!eng.ctx) { eng._init(); }
        var ctx = eng.ctx;
        if (!ctx) return;
        if (ctx.state === 'suspended') ctx.resume();
        var osc = ctx.createOscillator();
        var gain = ctx.createGain();
        osc.type = type || 'sine';
        osc.frequency.setValueAtTime(freq, ctx.currentTime);
        gain.gain.setValueAtTime(0.0001, ctx.currentTime);
        gain.gain.linearRampToValueAtTime(0.11, ctx.currentTime + 0.015);
        gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + (ms || 180) / 1000);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + (ms || 180) / 1000 + 0.02);
      } catch (e) { /* ignore */ }
    }
  };

  function toggleMute() {
    var muted = false;
    if (window.quizAudio) { muted = window.quizAudio.toggleMute(); }
    var btn = $('qmgSoundBtn');
    if (btn) btn.textContent = muted ? '🔇' : '🔊';
    if (!muted) audio.tick();
  }

  function syncMuteBtn() {
    var btn = $('qmgSoundBtn');
    if (!btn) return;
    var muted = false;
    try { muted = localStorage.getItem('qm_audio_muted') === 'true'; } catch (e) { }
    btn.textContent = muted ? '🔇' : '🔊';
  }

  function haptic(ms) {
    try { if (navigator.vibrate) navigator.vibrate(ms || 18); } catch (e) { }
  }

  // --- score & HUD -------------------------------------------------------
  function setScore(value, opts) {
    var prev = score;
    score = Math.max(0, Math.round(value));
    var el = $('qmgScore');
    if (el) {
      el.textContent = score;
      if (score !== prev) {
        el.classList.remove('qmg-grow');
        void el.offsetWidth;
        el.classList.add('qmg-grow');
      }
    }
    if (opts && opts.popFrom && score > prev) {
      pop(opts.popFrom, '+' + (score - prev), 'ok');
    }
    return score;
  }

  function addScore(delta, popFrom) {
    var before = score;
    setScore(score + delta);
    if (popFrom && delta !== 0) {
      pop(popFrom, (delta > 0 ? '+' : '') + (score - before), delta > 0 ? 'ok' : 'bad');
    }
    return score;
  }

  function getScore() { return score; }

  function setMid(text) { var el = $('qmgMid'); if (el) el.textContent = text; }
  function setMidLabel(text) {
    var el = $('qmgMid');
    if (!el) return;
    var label = el.previousElementSibling;
    if (label) label.textContent = text;
  }
  function setMidBar(fraction) {
    var bar = $('qmgMidBar');
    if (bar) bar.style.width = Math.max(0, Math.min(1, fraction)) * 100 + '%';
  }

  function setBest(value) {
    best = value;
    var el = $('qmgBest');
    if (el) el.textContent = value;
  }

  // --- streak ------------------------------------------------------------
  function bumpCombo() {
    combo += 1;
    if (combo > bestCombo) bestCombo = combo;
    var pill = $('qmgCombo');
    var count = $('qmgComboCount');
    if (count) count.textContent = combo;
    if (pill) {
      if (combo >= 2) { pill.classList.remove('hidden'); } else { pill.classList.add('hidden'); }
    }
    if (combo >= 2) audio.tone(520 + Math.min(combo, 8) * 70, 110, 'triangle');
    return combo;
  }

  function resetCombo() {
    combo = 0;
    var pill = $('qmgCombo');
    if (pill) pill.classList.add('hidden');
  }

  function getCombo() { return combo; }
  function comboMultiplier() { return 1 + Math.min(combo, 10) * 0.25; }

  // --- effects -----------------------------------------------------------
  function pop(target, text, kind) {
    var layer = $('qmgPopLayer');
    if (!layer) return;
    var x = window.innerWidth / 2;
    var y = window.innerHeight * 0.4;
    if (target && target.getBoundingClientRect) {
      var r = target.getBoundingClientRect();
      x = r.left + r.width / 2;
      y = r.top + r.height / 2;
    } else if (target && typeof target.x === 'number') {
      x = target.x; y = target.y;
    }
    var span = document.createElement('span');
    span.className = 'qmg-pop';
    span.textContent = text;
    span.style.left = x + 'px';
    span.style.top = y + 'px';
    span.style.fontSize = (kind === 'big' ? '2rem' : '1.35rem');
    span.style.color = kind === 'bad' ? '#fb7185' : (kind === 'warn' ? '#fbbf24' : '#34d399');
    layer.appendChild(span);
    setTimeout(function () { if (span.parentNode) span.parentNode.removeChild(span); }, 950);
  }

  function shake(el) {
    if (!el) return;
    el.classList.remove('qmg-shake');
    void el.offsetWidth;
    el.classList.add('qmg-shake');
  }

  function flashOk(el) {
    if (!el) return;
    el.classList.remove('qmg-flash-ok');
    void el.offsetWidth;
    el.classList.add('qmg-flash-ok');
  }

  function confetti(count) {
    var layer = $('qmgPopLayer');
    if (!layer) return;
    var colours = ['#22d3ee', '#a855f7', '#f472b6', '#34d399', '#fbbf24'];
    var n = count || 70;
    for (var i = 0; i < n; i++) {
      var bit = document.createElement('span');
      bit.className = 'qmg-confetti';
      bit.style.left = Math.random() * 100 + 'vw';
      bit.style.background = colours[i % colours.length];
      bit.style.animationDuration = (1.5 + Math.random() * 1.4) + 's';
      bit.style.animationDelay = (Math.random() * 0.5) + 's';
      layer.appendChild(bit);
      (function (node) {
        setTimeout(function () { if (node.parentNode) node.parentNode.removeChild(node); }, 3600);
      })(bit);
    }
  }

  // --- countdown ---------------------------------------------------------
  function startTimer(seconds, onEnd) {
    stopTimer();
    timerTotal = seconds * 1000;
    timerEnd = Date.now() + timerTotal;
    onTimeout = onEnd;
    var lastWhole = -1;
    setMidLabel('Time');
    tickTimer();
    timerId = setInterval(tickTimer, 100);

    function tickTimer() {
      var left = Math.max(0, timerEnd - Date.now());
      var whole = Math.ceil(left / 1000);
      if (whole !== lastWhole) {
        lastWhole = whole;
        setMid(formatClock(left));
        if (whole <= 5 && whole > 0) audio.heartbeat();
      }
      setMidBar(timerTotal ? left / timerTotal : 0);
      if (left <= 0) {
        stopTimer();
        if (typeof onTimeout === 'function') onTimeout();
      }
    }
  }

  function addTime(seconds) {
    if (!timerId) return;
    timerEnd += seconds * 1000;
    timerTotal = Math.max(timerTotal, timerEnd - Date.now());
    if (seconds > 0) pop($('qmgMid'), '+' + seconds + 's', 'warn');
  }

  function stopTimer() {
    if (timerId) { clearInterval(timerId); timerId = null; }
  }

  function timeLeft() {
    return timerId ? Math.max(0, timerEnd - Date.now()) : 0;
  }

  function formatClock(ms) {
    var total = Math.ceil(ms / 1000);
    var m = Math.floor(total / 60);
    var s = total % 60;
    return m > 0 ? m + ':' + (s < 10 ? '0' : '') + s : String(s);
  }

  // A silent stopwatch, for games whose HUD slot is showing something other
  // than the clock. Returns a function giving elapsed whole seconds.
  function stopwatch() {
    var began = Date.now();
    return function () { return Math.round((Date.now() - began) / 1000); };
  }

  // A count-up stopwatch for the puzzles, where slower simply scores less.
  function startStopwatch() {
    stopTimer();
    var began = Date.now();
    timerTotal = 0;
    setMidLabel('Time');
    setMidBar(1);
    timerId = setInterval(function () {
      setMid(formatClock((Date.now() - began) + 999));
    }, 200);
    return function elapsedSeconds() { return Math.round((Date.now() - began) / 1000); };
  }

  // --- finish ------------------------------------------------------------
  /**
   * Show the overlay and bank the score.
   * opts: { title, sub, icon, detail: [..lines], win: bool, score: override }
   */
  function finish(opts) {
    opts = opts || {};
    stopTimer();
    var finalScore = typeof opts.score === 'number' ? Math.max(0, Math.round(opts.score)) : score;

    $('qmgOverlayIcon').textContent = opts.icon || (opts.win === false ? '⏱️' : '🏆');
    $('qmgOverlayTitle').textContent = opts.title || (opts.win === false ? 'Time Up' : 'Nice One!');
    $('qmgOverlaySub').textContent = opts.sub || '';
    $('qmgOverlayScore').textContent = finalScore;
    $('qmgOverlayBest').textContent = '';
    $('qmgOverlayRewards').classList.add('hidden');

    var detail = $('qmgOverlayDetail');
    detail.innerHTML = '';
    var lines = (opts.detail || []).slice();
    if (bestCombo >= 3) lines.push('Best streak: ' + bestCombo + ' in a row');
    lines.forEach(function (line) {
      var p = document.createElement('div');
      p.textContent = line;
      detail.appendChild(p);
    });

    var card = $('qmgOverlayCard');
    card.classList.remove('border-purple-500/50', 'border-emerald-400/60', 'border-rose-500/50');
    card.classList.add(opts.win === false ? 'border-rose-500/50' : 'border-emerald-400/60');

    $('qmgOverlay').classList.remove('hidden');

    if (opts.win === false) {
      audio.wrong();
    } else {
      audio.victory();
      confetti(finalScore > 0 ? 80 : 30);
    }
    haptic(opts.win === false ? 60 : 30);

    submitScore(finalScore);
  }

  function submitScore(finalScore) {
    if (!gameKey) return;
    fetch('/games/api/score', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ game: gameKey, score: finalScore })
    })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (!data || !data.ok) return;
        setBest(data.best);
        var bestLine = $('qmgOverlayBest');
        if (bestLine) {
          bestLine.textContent = data.improved
            ? '🎉 New personal best!'
            : 'Your best: ' + data.best;
          bestLine.className = data.improved
            ? 'text-[11px] font-black text-amber-300'
            : 'text-[11px] font-bold text-slate-400';
        }
        if (data.xp > 0) {
          $('qmgOverlayRewards').classList.remove('hidden');
          $('qmgOverlayXp').textContent = '+' + data.xp;
          $('qmgOverlayCoins').textContent = '+' + data.coins;
          $('qmgOverlayRank').textContent = '#' + data.rank;
        }
        if (data.improved) { confetti(50); }
        submitted = true;
      })
      .catch(function () { /* a lost score should never break the game */ });
  }

  function hideOverlay() { $('qmgOverlay').classList.add('hidden'); }

  function replay() {
    hideOverlay();
    resetCombo();
    bestCombo = 0;
    setScore(0);
    submitted = false;
    if (typeof replayFn === 'function') { replayFn(); } else { window.location.reload(); }
  }

  function onReplay(fn) { replayFn = fn; }

  // --- misc helpers ------------------------------------------------------
  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

  function normalise(text) {
    return String(text || '').toUpperCase().replace(/[^A-Z0-9]/g, '');
  }

  function sleep(ms) { return new Promise(function (res) { setTimeout(res, ms); }); }

  /**
   * Redraw an image as a filled square and hand back a data URL.
   *
   * The flags, badges and logos in the question bank are all sorts of shapes,
   * and a tile puzzle needs square tiles. Slicing a 3:2 flag straight into a
   * square grid leaves white bands through the picture, so we centre-crop it
   * onto a square canvas once and slice that instead. Falls back to the
   * original URL if the image will not draw.
   */
  function squareImage(url, size) {
    size = size || 600;
    return new Promise(function (resolve) {
      var img = new Image();
      img.crossOrigin = 'anonymous';
      img.onload = function () {
        try {
          var canvas = document.createElement('canvas');
          canvas.width = canvas.height = size;
          var ctx = canvas.getContext('2d');
          ctx.fillStyle = '#ffffff';
          ctx.fillRect(0, 0, size, size);
          var w = img.naturalWidth || img.width || size;
          var h = img.naturalHeight || img.height || size;
          var scale = Math.max(size / w, size / h);
          var dw = w * scale, dh = h * scale;
          ctx.drawImage(img, (size - dw) / 2, (size - dh) / 2, dw, dh);
          resolve(canvas.toDataURL('image/png'));
        } catch (e) {
          resolve(url);
        }
      };
      img.onerror = function () { resolve(url); };
      img.src = url;
    });
  }

  function init(opts) {
    gameKey = (opts && opts.gameKey) || '';
    best = (opts && opts.best) || 0;
    syncMuteBtn();
    setScore(0);
    // Any first tap unlocks the Web Audio context on iOS.
    document.addEventListener('pointerdown', function unlock() {
      audio.call('_init');
      document.removeEventListener('pointerdown', unlock);
    }, { once: true });
  }

  return {
    init: init, audio: audio, toggleMute: toggleMute, haptic: haptic,
    setScore: setScore, addScore: addScore, getScore: getScore, setBest: setBest,
    setMid: setMid, setMidLabel: setMidLabel, setMidBar: setMidBar,
    bumpCombo: bumpCombo, resetCombo: resetCombo, getCombo: getCombo, comboMultiplier: comboMultiplier,
    pop: pop, shake: shake, flashOk: flashOk, confetti: confetti,
    startTimer: startTimer, stopTimer: stopTimer, addTime: addTime, timeLeft: timeLeft,
    startStopwatch: startStopwatch, stopwatch: stopwatch, formatClock: formatClock,
    finish: finish, replay: replay, onReplay: onReplay, hideOverlay: hideOverlay,
    shuffle: shuffle, pick: pick, normalise: normalise, sleep: sleep,
    squareImage: squareImage
  };
})();
