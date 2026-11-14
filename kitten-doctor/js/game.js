/**
 * Доктор для котёнка — основная логика игры.
 * Управление: тап/клик по крупным кнопкам и объектам.
 */
(function () {
  "use strict";

  var STEPS = ["start", "exam", "wash", "medicine", "bandage", "feed", "win"];
  var PROGRESS = {
    start: 0,
    exam: 12,
    wash: 28,
    medicine: 48,
    bandage: 68,
    feed: 85,
    win: 100
  };

  var state = {
    screen: "start",
    selectedTool: null,
    washDone: false,
    medDone: false,
    bandageDone: false,
    feedDone: false
  };

  var els = {};

  function $(id) {
    return document.getElementById(id);
  }

  function cacheEls() {
    els.progressFill = $("progressFill");
    els.progress = $("progress");
    els.screens = {};
    STEPS.forEach(function (name) {
      els.screens[name] = $("screen-" + name);
    });
  }

  function setProgress(screen) {
    var value = PROGRESS[screen] || 0;
    if (els.progressFill) {
      els.progressFill.style.width = value + "%";
    }
    if (els.progress) {
      els.progress.setAttribute("aria-valuenow", String(value));
    }
  }

  function showScreen(name) {
    state.screen = name;
    state.selectedTool = null;

    STEPS.forEach(function (key) {
      var node = els.screens[key];
      if (!node) return;
      if (key === name) {
        node.hidden = false;
        node.classList.add("screen--active");
      } else {
        node.hidden = true;
        node.classList.remove("screen--active");
      }
    });

    document.querySelectorAll(".tool-btn").forEach(function (btn) {
      btn.setAttribute("aria-pressed", "false");
    });

    setProgress(name);

    var bridge = window.YandexGamesBridge;
    if (bridge) {
      if (name === "exam") bridge.gameplayStart();
      if (name === "win") bridge.gameplayStop();
    }
  }

  function setFeedback(id, text, kind) {
    var node = $(id);
    if (!node) return;
    node.textContent = text || "";
    node.classList.remove("is-ok", "is-error");
    if (kind) node.classList.add(kind);
  }

  function selectTool(btn) {
    var tool = btn.getAttribute("data-tool");
    state.selectedTool = tool;
    document.querySelectorAll(".tool-btn").forEach(function (b) {
      b.setAttribute("aria-pressed", b === btn ? "true" : "false");
    });
  }

  function goNext(from) {
    var idx = STEPS.indexOf(from);
    if (idx < 0 || idx >= STEPS.length - 1) return;
    showScreen(STEPS[idx + 1]);
  }

  function softDelay(fn, ms) {
    window.setTimeout(fn, ms || 700);
  }

  /* ——— Осмотр ——— */
  function onExamHotspot(e) {
    var target = e.currentTarget;
    var id = target.id;

    if (id === "hotspotPaw") {
      target.classList.add("is-correct");
      setFeedback("examFeedback", "Да! Болит правая лапка.", "is-ok");
      softDelay(function () {
        goNext("exam");
      }, 850);
      return;
    }

    target.classList.add("is-wrong");
    setFeedback("examFeedback", "Не здесь. Попробуй нажать на лапку!", "is-error");
    softDelay(function () {
      target.classList.remove("is-wrong");
    }, 400);
  }

  /* ——— Мытьё ——— */
  function onWashPaw() {
    if (state.washDone) return;
    if (state.selectedTool !== "soap") {
      setFeedback("washFeedback", "Сначала нажми на мыло!", "is-error");
      return;
    }
    state.washDone = true;
    var bubbles = $("bubbles");
    if (bubbles) bubbles.hidden = false;
    $("toolSoap").classList.add("is-used");
    $("toolSoap").setAttribute("aria-pressed", "false");
    state.selectedTool = null;
    setFeedback("washFeedback", "Лапку помыли! Чисто!", "is-ok");
    softDelay(function () {
      goNext("wash");
    }, 900);
  }

  /* ——— Лекарство ——— */
  function onGiveMed() {
    if (state.medDone) return;
    if (state.selectedTool !== "medicine") {
      setFeedback("medFeedback", "Сначала возьми лекарство!", "is-error");
      return;
    }
    state.medDone = true;
    $("toolMed").classList.add("is-used");
    $("toolMed").setAttribute("aria-pressed", "false");
    state.selectedTool = null;
    setFeedback("medFeedback", "Котёнок выпил лекарство. Умница!", "is-ok");
    softDelay(function () {
      goNext("medicine");
    }, 900);
  }

  /* ——— Пластырь ——— */
  function onApplyBandage() {
    if (state.bandageDone) return;
    if (state.selectedTool !== "bandage") {
      setFeedback("bandageFeedback", "Сначала возьми пластырь!", "is-error");
      return;
    }
    state.bandageDone = true;
    var patch = $("bandagePatch");
    if (patch) patch.hidden = false;
    $("toolBandage").classList.add("is-used");
    $("toolBandage").setAttribute("aria-pressed", "false");
    state.selectedTool = null;
    setFeedback("bandageFeedback", "Пластырь на месте!", "is-ok");
    softDelay(function () {
      goNext("bandage");
    }, 900);
  }

  /* ——— Кормление ——— */
  function onFeed() {
    if (state.feedDone) return;
    state.feedDone = true;
    var bowl = $("btnBowl");
    if (bowl) bowl.classList.add("is-empty");
    setFeedback("feedFeedback", "Ням-ням! Котёнок сыт и счастлив!", "is-ok");
    softDelay(function () {
      showScreen("win");
      spawnConfetti();
    }, 900);
  }

  function spawnConfetti() {
    var box = $("confetti");
    if (!box) return;
    box.innerHTML = "";
    var colors = ["#ff9b7a", "#5bb8b0", "#ffe066", "#ff8fa3", "#7ad4ef", "#8bc34a"];
    for (var i = 0; i < 36; i++) {
      var piece = document.createElement("span");
      piece.style.left = Math.random() * 100 + "%";
      piece.style.background = colors[i % colors.length];
      piece.style.animationDuration = 1.4 + Math.random() * 1.6 + "s";
      piece.style.animationDelay = Math.random() * 0.6 + "s";
      piece.style.width = 8 + Math.random() * 8 + "px";
      piece.style.height = 10 + Math.random() * 10 + "px";
      box.appendChild(piece);
    }
  }

  function resetGame() {
    state = {
      screen: "start",
      selectedTool: null,
      washDone: false,
      medDone: false,
      bandageDone: false,
      feedDone: false
    };

    ["examFeedback", "washFeedback", "medFeedback", "bandageFeedback", "feedFeedback"].forEach(
      function (id) {
        setFeedback(id, "");
      }
    );

    document.querySelectorAll(".tool-btn").forEach(function (btn) {
      btn.classList.remove("is-used");
      btn.setAttribute("aria-pressed", "false");
    });

    document.querySelectorAll(".hotspot").forEach(function (h) {
      h.classList.remove("is-correct", "is-wrong");
    });

    var bubbles = $("bubbles");
    if (bubbles) bubbles.hidden = true;
    var patch = $("bandagePatch");
    if (patch) patch.hidden = true;
    var bowl = $("btnBowl");
    if (bowl) bowl.classList.remove("is-empty");
    var confetti = $("confetti");
    if (confetti) confetti.innerHTML = "";

    showScreen("start");
  }

  function bind() {
    $("btnStart").addEventListener("click", function () {
      showScreen("exam");
    });
    $("btnReplay").addEventListener("click", resetGame);

    ["hotspotPaw", "hotspotHead", "hotspotBody"].forEach(function (id) {
      var node = $(id);
      if (node) node.addEventListener("click", onExamHotspot);
    });

    $("toolSoap").addEventListener("click", function () {
      if (state.washDone) return;
      selectTool(this);
      setFeedback("washFeedback", "Мыло в руках! Теперь нажми на лапку.", "is-ok");
    });
    $("washPaw").addEventListener("click", onWashPaw);

    $("toolMed").addEventListener("click", function () {
      if (state.medDone) return;
      selectTool(this);
      setFeedback("medFeedback", "Лекарство готово! Нажми на котёнка.", "is-ok");
    });
    $("giveMed").addEventListener("click", onGiveMed);

    $("toolBandage").addEventListener("click", function () {
      if (state.bandageDone) return;
      selectTool(this);
      setFeedback("bandageFeedback", "Пластырь готов! Нажми на лапку.", "is-ok");
    });
    $("applyBandage").addEventListener("click", onApplyBandage);

    $("btnBowl").addEventListener("click", onFeed);
  }

  function init() {
    cacheEls();
    bind();
    showScreen("start");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
