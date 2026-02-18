from appium import webdriver
from appium.options.android import UiAutomator2Options
import time
import pytest

# Функция для тапа
def tap(x, y):
    driver.execute_script('mobile: clickGesture', {'x': x, 'y': y})

def test_start_game():
    # Настройки
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "Твое устройство"
    options.app_package = "com.money.empire.business.tycoon.casual.strategy.game.lifestyle.simulation.rich.businessman"
    options.app_activity = "com.cocos.game.AppActivity"
    options.automation_name = "UiAutomator2"
    options.no_reset = True

    # Подключаемся к серверу
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

    try:
        # Получаем текущее приложение
        current_app = driver.current_package
        if current_app == options.app_package:
            # Активируем приложение МО
            driver.activate_app(options.app_package)
        else:
            # Запущено другое приложение, запускаю игру
            driver.execute_script('mobile: startActivity', {
                'intent': f'{options.app_package}/{options.app_activity}'
            })
    except Exception as e:
        print(f"Ошибка при проверке: {e}")
        print("Пробую запустить игру напрямую...")
        # Запасной вариант запуска
        driver.execute_script('mobile: startActivity', {
            'intent': f'{options.app_package}/{options.app_activity}'
        })
        print("Игра запущена")
        time.sleep(15)

def test_button_new_game():
    play_button_x = 500
    play_button_y = 2100
    tap(play_button_x, play_button_y)