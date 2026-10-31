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

  // A burst of sparks out of one element, for the moment a tap pays off.
  // Confetti rains on the whole screen and belongs to the end of a game; this
  // is the small, cheap reward you get dozens of times inside one.
  function burst(target, opts) {
    var layer = $('qmgPopLayer');
    if (!layer || !target || !target.getBoundingClientRect) return;
    opts = opts || {};
    var r = target.getBoundingClientRect();
    var x = r.left + r.width / 2;
    var y = r.top + r.height / 2;
    var colours = opts.colours || ['#22d3ee', '#a855f7', '#fbbf24', '#34d399'];
    var n = opts.count || 10;
    for (var i = 0; i < n; i++) {
      var spark = document.createElement('span');
      spark.className = 'qmg-spark';
      var angle = (Math.PI * 2 * i) / n + Math.random() * 0.4;
      var dist = (opts.spread || 42) * (0.6 + Math.random() * 0.7);
      spark.style.left = x + 'px';
      spark.style.top = y + 'px';
      spark.style.background = colours[i % colours.length];
      spark.style.setProperty('--dx', Math.cos(angle) * dist + 'px');
      spark.style.setProperty('--dy', Math.sin(angle) * dist + 'px');
      layer.appendChild(spark);
      (function (node) {
        setTimeout(function () { if (node.parentNode) node.parentNode.removeChild(node); }, 700);
      })(spark);
    }
  }

  // A wash of colour in from the screen edges. Felt rather than read, so it
  // carries right or wrong even when your eyes are on the board.
  function glow(kind) {
    var el = $('qmgGlow');
    if (!el) return;
    el.className = 'qmg-glow qmg-glow-' + (kind === 'bad' ? 'bad' : (kind === 'gold' ? 'gold' : 'ok'));
    void el.offsetWidth;
    el.classList.add('qmg-glow-on');
    setTimeout(function () { el.classList.remove('qmg-glow-on'); }, 480);
  }

  // The streak banner. A pill counting up is information; this is a reward,
  // so it only fires at the milestones and gets louder as they climb.
  var STREAK_TIERS = [
    { at: 3, label: 'NICE RUN', icon: '✨', pitch: 620 },
    { at: 5, label: 'ON FIRE', icon: '🔥', pitch: 720 },
    { at: 8, label: 'UNSTOPPABLE', icon: '⚡', pitch: 840 },
    { at: 12, label: 'LEGENDARY', icon: '👑', pitch: 980 }
  ];

  function streakTier(n) {
    var tier = null;
    for (var i = 0; i < STREAK_TIERS.length; i++) {
      if (n === STREAK_TIERS[i].at) tier = STREAK_TIERS[i];
    }
    return tier;
  }

  function banner(text, icon, kind) {
    var el = $('qmgBanner');
    if (!el) return;
    el.innerHTML = '';
    var span = document.createElement('span');
    span.textContent = (icon ? icon + ' ' : '') + text;
    el.appendChild(span);
    el.className = 'qmg-banner qmg-banner-' + (kind || 'hot');
    void el.offsetWidth;
    el.classList.add('qmg-banner-on');
    setTimeout(function () { el.classList.remove('qmg-banner-on'); }, 1100);
  }

  // Call instead of bumpCombo where the game wants the celebration too.
  function reward(target) {
    var n = bumpCombo();
    var tier = streakTier(n);
    if (tier) {
      banner(tier.label + ' ×' + n, tier.icon, n >= 8 ? 'gold' : 'hot');
      glow(n >= 8 ? 'gold' : 'ok');
      confetti(n >= 8 ? 40 : 18);
      audio.tone(tier.pitch, 220, 'triangle');
      haptic(45);
    } else if (target) {
      burst(target);
    }
    return n;
  }

  // Count a number up rather than printing it. The end of a game is the one
  // moment worth drawing out, and a ticking total reads as a reward where the
  // finished figure reads as a receipt.
  function countUp(el, to, ms) {
    if (!el) return;
    var target = Math.max(0, Math.round(to));
    if (!target) { el.textContent = '0'; return; }
    var duration = ms || 900;
    var started = 0;
    function frame(now) {
      if (!started) started = now;
      var t = Math.min(1, (now - started) / duration);
      // Ease out, so it races away and settles rather than crawling.
      var eased = 1 - Math.pow(1 - t, 3);
      el.textContent = Math.round(target * eased);
      if (t < 1) requestAnimationFrame(frame);
      else el.textContent = target;
    }
    requestAnimationFrame(frame);
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
    countUp($('qmgOverlayScore'), finalScore);
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
      glow('bad');
    } else {
      audio.victory();
      confetti(finalScore > 0 ? 80 : 30);
      glow('gold');
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
        if (data.improved) {
          confetti(50);
          banner('NEW PERSONAL BEST', '🏅', 'gold');
          haptic(70);
        }
        if (data.xp > 0) {
          countUp($('qmgOverlayXp'), data.xp, 700);
          var xpEl = $('qmgOverlayXp');
          // countUp writes the bare number, so put the plus back after it.
          setTimeout(function () {
            if (xpEl) xpEl.textContent = '+' + data.xp;
          }, 760);
        }
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

  /**
   * Word checking, in two tiers.
   *
   * The page loads a small common-word list, which answers almost every guess
   * instantly. Anything it does not recognise goes to the server, which holds
   * the full 315,000 word dictionary in memory. If that call fails we accept
   * the word: wrongly rejecting something a player actually typed is worse
   * than letting an odd one through.
   */
  var localWords = null;
  var wordCache = {};

  function loadWords(url) {
    return fetch(url || '/static/data/qm-lexicon.json')
      .then(function (r) { return r.json(); })
      .then(function (list) {
        localWords = {};
        list.forEach(function (w) { localWords[w.toLowerCase()] = true; });
        return localWords;
      })
      .catch(function () { localWords = null; });
  }

  function checkWord(word) {
    var w = String(word || '').toLowerCase().replace(/[^a-z]/g, '');
    if (!w) return Promise.resolve(false);
    if (localWords && localWords[w]) return Promise.resolve(true);
    if (w in wordCache) return Promise.resolve(wordCache[w]);

    return fetch('/games/api/check-word', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ word: w })
    })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        var valid = !!(data && data.valid);
        wordCache[w] = valid;
        return valid;
      })
      .catch(function () { return true; });
  }

  // -------------------------------------------------------------------------
  // On screen keyboard
  //
  // Games that take letters draw their own rather than asking for the device
  // keyboard. On a phone the system keyboard costs far more than it gives: it
  // covers half the screen, it zooms the page in on any input whose text is
  // under 16px, and it shrinks the visual viewport enough to confuse anything
  // measuring the window. None of that happens with buttons.
  // -------------------------------------------------------------------------

  var KEY_ROWS = ['QWERTYUIOP', 'ASDFGHJKL', 'ZXCVBNM'];

  function keyboard(host, opts) {
    opts = opts || {};
    var onKey = opts.onKey || function () {};
    var states = {};
    // A game whose letters are given to you - an anagram, a word wheel, the
    // vowels put back into a phrase - wants those letters and no others. A
    // full alphabet there is just twenty spare keys to look past.
    var rows = opts.rows || KEY_ROWS;

    function keyClass(state) {
      var base = 'flex-1 min-w-0 h-11 rounded-lg font-mono font-black text-sm transition select-none ';
      if (state === 'hit') return base + 'bg-emerald-500 text-slate-950';
      if (state === 'near') return base + 'bg-amber-500 text-slate-950';
      if (state === 'miss') return base + 'bg-slate-800 text-slate-600';
      return base + 'bg-slate-900 border border-purple-500/30 text-slate-100 active:bg-purple-900/70';
    }

    function wideKey(label, value, tone) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'px-2.5 h-11 rounded-lg bg-slate-900 border border-purple-500/30 font-mono ' +
        'font-black text-[10px] active:bg-purple-900/70 transition shrink-0 select-none ' +
        (tone || 'text-cyan-300');
      btn.textContent = label;
      tap(btn, value);
      return btn;
    }

    // Keys fire on pointerdown so a fast typist is not waiting on the 300ms
    // the browser spends deciding whether a tap was a double tap.
    function tap(btn, value) {
      btn.addEventListener('pointerdown', function (ev) {
        ev.preventDefault();
        onKey(value);
      });
      btn.addEventListener('click', function (ev) { ev.preventDefault(); });
    }

    function render() {
      host.innerHTML = '';
      host.className = 'space-y-1.5 qmg-nosel';
      var last = rows.length - 1;
      rows.forEach(function (row, idx) {
        var line = document.createElement('div');
        line.className = 'flex gap-1.5 justify-center';
        if (idx === last && opts.enter !== false) {
          line.appendChild(wideKey(opts.enterLabel || 'ENTER', 'ENTER'));
        }
        row.split('').forEach(function (ch) {
          var btn = document.createElement('button');
          btn.type = 'button';
          btn.className = keyClass(states[ch] || 'idle');
          btn.textContent = ch;
          tap(btn, ch);
          line.appendChild(btn);
        });
        if (idx === last) {
          line.appendChild(wideKey('⌫', 'BACK', 'text-rose-300'));
        }
        host.appendChild(line);
      });
    }

    render();

    return {
      el: host,
      render: render,
      setStates: function (map) { states = map || {}; render(); },
      setRows: function (next) { rows = next || KEY_ROWS; render(); },
      // Physical keyboards still work, for anyone on a desktop.
      bindPhysical: function () {
        document.addEventListener('keydown', function (ev) {
          if (ev.metaKey || ev.ctrlKey || ev.altKey) return;
          if (ev.key === 'Enter') { ev.preventDefault(); onKey('ENTER'); return; }
          if (ev.key === 'Backspace') { ev.preventDefault(); onKey('BACK'); return; }
          if (/^[a-zA-Z]$/.test(ev.key)) { ev.preventDefault(); onKey(ev.key.toUpperCase()); return; }
          if (ev.key.indexOf('Arrow') === 0) { ev.preventDefault(); onKey(ev.key); }
        });
      }
    };
  }

  // -------------------------------------------------------------------------
  // Board gestures
  //
  // Locks the board against the page: touch-action none is what actually stops
  // a phone scrolling the page while a finger is dragging across a grid, since
  // preventDefault on a pointer event cannot do it on its own.
  //
  // Then a tap and a swipe both count. On a sliding puzzle a tile next to the
  // gap can only go one way, so the direction of the swipe does not need
  // reading: starting the gesture on a tile is enough to say which one to move.
  // -------------------------------------------------------------------------

  // Hang a keyboard of ours onto a game that already has a text box and a
  // form. The game's own submit handler is left exactly as it was: the keys
  // simply type into the box and press go, which is all the device keyboard
  // was ever doing.
  //
  // On a touch screen the box is made read only so tapping it cannot raise
  // the system keyboard over the game. On a desktop it stays an ordinary
  // input, because typing on real keys should still work.
  function attachKeyboard(host, input, form, opts) {
    if (!host || !input) return null;
    opts = opts || {};
    var coarse = !(window.matchMedia && window.matchMedia('(pointer: fine)').matches);
    if (coarse) {
      input.readOnly = true;
      input.setAttribute('inputmode', 'none');
    }

    function submit() {
      if (!form) return;
      if (form.requestSubmit) form.requestSubmit();
      else form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    }

    return keyboard(host, {
      rows: opts.rows,
      enterLabel: opts.enterLabel || 'ENTER',
      onKey: function (k) {
        if (k === 'BACK') {
          input.value = input.value.slice(0, -1);
        } else if (k === 'ENTER') {
          submit();
        } else if (/^[A-Z]$/.test(k)) {
          if (opts.maxLength && input.value.length >= opts.maxLength) return;
          input.value += k;
          audio.tick();
        } else {
          return;
        }
        if (opts.onChange) opts.onChange(input.value);
      }
    });
  }

  // Put the cursor in a box, but only where that is a kindness. On a desktop
  // it saves a click. On a phone it throws the keyboard up over the game
  // without being asked, which is what used to happen after every submit.
  function softFocus(el) {
    if (!el) return;
    var fine = window.matchMedia && window.matchMedia('(pointer: fine)').matches;
    if (fine) el.focus({ preventScroll: true });
  }

  function boardGestures(el, onPick) {
    if (!el) return;
    el.style.touchAction = 'none';
    var startNode = null;

    el.addEventListener('pointerdown', function (ev) {
      startNode = ev.target.closest('[data-pos]');
      if (startNode) ev.preventDefault();
    });

    el.addEventListener('pointerup', function (ev) {
      var endNode = ev.target.closest('[data-pos]');
      var node = startNode || endNode;
      startNode = null;
      if (!node) return;
      ev.preventDefault();
      onPick(parseInt(node.dataset.pos, 10), node);
    });

    el.addEventListener('pointercancel', function () { startNode = null; });
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
    burst: burst, glow: glow, banner: banner, reward: reward, countUp: countUp,
    startTimer: startTimer, stopTimer: stopTimer, addTime: addTime, timeLeft: timeLeft,
    startStopwatch: startStopwatch, stopwatch: stopwatch, formatClock: formatClock,
    finish: finish, replay: replay, onReplay: onReplay, hideOverlay: hideOverlay,
    shuffle: shuffle, pick: pick, normalise: normalise, sleep: sleep,
    squareImage: squareImage, loadWords: loadWords, checkWord: checkWord,
    keyboard: keyboard, attachKeyboard: attachKeyboard,
    boardGestures: boardGestures, softFocus: softFocus
  };
})();
