import os
import cv2
import numpy as np
import pytest
import time

def _get_screenshot_bgr(driver) -> np.ndarray:
    png = driver.get_screenshot_as_png()
    img = cv2.imdecode(np.frombuffer(png, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise RuntimeError("Не удалось декодировать screenshot")
    return img


def find_on_screen_multiscale(
    driver,
    template_path: str,
    threshold: float = 0.78,
    scales=(0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.20),
    method=cv2.TM_CCOEFF_NORMED,
):
    # 1) Загружаем шаблон
    template_bgr = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template_bgr is None:
        raise RuntimeError(f"Не удалось загрузить шаблон: {template_path}")

    # 2) Берём скрин и переводим всё в grayscale (менее чувствительно к оттенкам)
    screen_bgr = _get_screenshot_bgr(driver)
    screen_g = cv2.cvtColor(screen_bgr, cv2.COLOR_BGR2GRAY)
    tpl_g0 = cv2.cvtColor(template_bgr, cv2.COLOR_BGR2GRAY)

    best_score = -1.0
    best_center = None

    # 3) Перебираем масштабы шаблона
    for s in scales:
        tpl_g = cv2.resize(tpl_g0, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
        th, tw = tpl_g.shape[:2]
        sh, sw = screen_g.shape[:2]

        if th >= sh or tw >= sw:
            continue

        res = cv2.matchTemplate(screen_g, tpl_g, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        score = max_val if method in (cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR_NORMED) else -min_val
        loc = max_loc if method in (cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR_NORMED) else min_loc

        if score > best_score:
            x, y = loc
            best_score = score
            best_center = (x + tw // 2, y + th // 2)

    # 4) Проверяем уверенность
    if best_center is None or best_score < threshold:
        raise RuntimeError(f"Кнопка не найдена. best_confidence={best_score:.3f}")

    return best_center[0], best_center[1], best_score


def tap_xy(driver, x, y):
    driver.execute_script("mobile: clickGesture", {"x": int(x), "y": int(y)})


# ---------- waits ----------

def wait_for_template(
    driver,
    template_path,
    timeout=60,
    threshold=0.78,
    poll=1.0,
):
    start = time.time()
    last_err = None
    while time.time() - start < timeout:
        try:
            return find_on_screen_multiscale(driver, template_path, threshold=threshold)
        except RuntimeError as e:
            last_err = e
            time.sleep(poll)
    raise RuntimeError(f"{template_path} не появился за {timeout} секунд. last={last_err}")


def wait_until_gone(
    driver,
    template_path,
    timeout=60,
    threshold=0.78,
    poll=1.0,
    require_seen=False,
):
    """
    require_seen=True:
      сначала ждём, что шаблон хотя бы раз появился,
      и только после этого ждём исчезновения.
      Это убирает ложное "исчез", когда loading.png просто не находился.
    """
    start = time.time()
    seen = False

    while time.time() - start < timeout:
        try:
            find_on_screen_multiscale(driver, template_path, threshold=threshold)
            seen = True
            time.sleep(poll)
        except RuntimeError:
            if not require_seen or seen:
                return True
            time.sleep(poll)

    if require_seen and not seen:
        raise RuntimeError(f"{template_path} так и не был обнаружен за {timeout} секунд")
    raise RuntimeError(f"{template_path} не исчез за {timeout} секунд")


# ---------- test ----------

def test_tap_play(app_driver):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    loading_path = os.path.join(BASE_DIR, "../assets", "loading_screen.png")
    button_path = os.path.join(BASE_DIR, "../assets", "new_game_button_start_screen.png")

    # 1) Пытаемся дождаться загрузочного экрана и его исчезновения
    # Если loading не нашли — не валим тест, просто переходим к ожиданию кнопки
    try:
        wait_for_template(app_driver, loading_path, timeout=12, threshold=0.80, poll=1.0)
        print("Загрузочный экран обнаружен")

        wait_until_gone(app_driver, loading_path, timeout=90, threshold=0.80, poll=1.0, require_seen=True)
        print("Загрузочный экран исчез")
    except RuntimeError:
        print("Загрузочный экран не подтверждён, ждём кнопку напрямую")

    # 2) Ждём появления кнопки (multiscale)
    x, y, conf = wait_for_template(app_driver, button_path, timeout=90, threshold=0.78, poll=1.0)
    print(f"Кнопка найдена conf={conf:.3f} в точке ({x}, {y})")

    # 3) Нажимаем
    tap_xy(app_driver, x, y)

    # 4) Проверяем, что кнопка исчезла (даём экрану обновиться)
    time.sleep(1.0)
    with pytest.raises(RuntimeError):
        find_on_screen_multiscale(app_driver, button_path, threshold=0.80)