import os
import time
import subprocess
import pytest
import requests
import shutil

from appium import webdriver
from appium.options.android import UiAutomator2Options


APPIUM_HOST = os.getenv("APPIUM_HOST", "127.0.0.1")
APPIUM_PORT = int(os.getenv("APPIUM_PORT", "4723"))
APPIUM_URL = f"http://{APPIUM_HOST}:{APPIUM_PORT}"
STATUS_URL = f"{APPIUM_URL}/status"

#Параметр управления логами
APPIUM_LOG_MODE = os.getenv("APPIUM_LOG_MODE", "off")
# off | error | file | console

def wait_for_appium(max_wait_seconds: int = 30) -> None:
    start = time.time()
    while time.time() - start < max_wait_seconds:
        try:
            r = requests.get(STATUS_URL, timeout=2)
            if r.status_code == 200:
                return
        except Exception:
            pass
        time.sleep(1)
    raise RuntimeError("Appium не стартовал за отведённое время")


@pytest.fixture(scope="session", autouse=True)
def appium_server():
    appium_exe = shutil.which("appium") or shutil.which("appium.cmd")
    if not appium_exe:
        raise RuntimeError(
            "Команда appium не найдена в PATH. "
            "Проверь: npm i -g appium и путь C:\\Users\\User\\AppData\\Roaming\\npm в PATH."
        )

    cmd = [appium_exe, "--port", str(APPIUM_PORT)]

    #Управление логированием сервера
    if APPIUM_LOG_MODE == "off":
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    elif APPIUM_LOG_MODE == "error":
        cmd += ["--log-level", "error"]
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    elif APPIUM_LOG_MODE == "file":
        cmd += ["--log-level", "info"]
        log_file = open("appium.log", "w", encoding="utf-8")
        process = subprocess.Popen(
            cmd,
            stdout=log_file,
            stderr=subprocess.STDOUT
        )

    else:  # console
        process = subprocess.Popen(cmd)

    wait_for_appium()
    yield

    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()


@pytest.fixture(scope="session", autouse=True)
def app_driver(appium_server):
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"

    options.app_package = "com.money.empire.business.tycoon.casual.strategy.game.lifestyle.simulation.rich.businessman"
    options.app_activity = "com.cocos.game.AppActivity"

    options.no_reset = os.getenv("ANDROID_NO_RESET", "true").lower() == "true"
    options.new_command_timeout = int(os.getenv("ANDROID_NEW_COMMAND_TIMEOUT", "120"))

    driver = webdriver.Remote(APPIUM_URL, options=options)

    time.sleep(2)

    yield driver

    driver.quit()