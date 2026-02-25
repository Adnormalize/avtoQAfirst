'''
from appium import webdriver
from appium.options.android import UiAutomator2Options
import time
import pytest

# Вспомогательная функция для тапа по координатам
def tap(driver, x, y):
    driver.execute_script("mobile: clickGesture", {'x': x, 'y': y})

# Хранит координаты кнопок гоавного экрана
@pytest.fixture()
def game_coordinates():
    return {
        "new_game": {'x': 500, 'y': 2100},
        "continue": {'x': 538, 'y': 1923},
    }

@pytest.fixture(scope="function")
def game_driver():

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
    driver.app_package = options.app_package
    driver.app_activity = options.app_activity

    # Передаем управление тесту
    yield driver

    # Очистка после теста
    driver.quit()

def test_button_new_game(game_driver, game_coordinates):

    driver = game_driver

    coords = game_coordinates['new_game']
    tap(driver, coords['x'], coords['y'])
'''