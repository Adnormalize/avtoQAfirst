/**
 * Заглушка под будущую интеграцию Яндекс Игр.
 * Без рекламы и без реального SDK.
 *
 * Когда будете подключать настоящий SDK:
 * 1. Добавьте <script src="/sdk.js"></script> перед этим файлом
 *    (или замените этот файл на инициализацию YaGames.init()).
 * 2. Используйте window.YandexGamesBridge ниже для Game Ready / gameplay API.
 * 3. Рекламу (showFullscreenAdv / rewarded) НЕ подключаем на этом этапе.
 */
(function (global) {
  "use strict";

  var stub = {
    isStub: true,
    ready: true,
    /** Сообщить платформе, что игра готова (заглушка). */
    gameReady: function () {
      if (global.console && console.info) {
        console.info("[YandexGamesBridge] gameReady (stub)");
      }
    },
    /** Начало / конец геймплея — для будущей аналитики платформы. */
    gameplayStart: function () {
      if (global.console && console.info) {
        console.info("[YandexGamesBridge] gameplayStart (stub)");
      }
    },
    gameplayStop: function () {
      if (global.console && console.info) {
        console.info("[YandexGamesBridge] gameplayStop (stub)");
      }
    },
    /**
     * Место под рекламу — намеренно пустое.
     * Не вызывать showFullscreenAdv / rewarded до явного решения.
     */
    ads: {
      enabled: false,
      showFullscreen: function () {
        return Promise.resolve({ shown: false, reason: "ads-disabled" });
      },
      showRewarded: function () {
        return Promise.resolve({ shown: false, reason: "ads-disabled" });
      }
    }
  };

  global.YandexGamesBridge = stub;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      stub.gameReady();
    });
  } else {
    stub.gameReady();
  }
})(typeof window !== "undefined" ? window : this);
