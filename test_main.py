from appium import webdriver
from appium.options.android import UiAutomator2Options
import time

options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "Твое устройство"
options.app_package = "com.money.empire.business.tycoon.casual.strategy.game.lifestyle.simulation.rich.businessman"
options.app_activity = "com.cocos.game.AppActivity"
options.automation_name = "UiAutomator2"
options.no_reset = True

driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
print("Игра запущена!")

buttons = driver.find_elements(by=AppiumBy.CLASS_NAME, value="android.widget.Button")

for i, btn in enumerate(buttons):
    loc = btn.location
    size = btn.size

    # Координаты в пикселях
    center_x = loc['x'] + size['width'] // 2
    center_y = loc['y'] + size['height'] // 2

    # Переводим в проценты
    percent_x = (center_x / driver.screen_width) * 100
    percent_y = (center_y / driver.screen_height) * 100

    print(f"\nКнопка {i}: '{btn.text}'")
    print(f"  Пиксели: ({center_x}, {center_y})")
    print(f"  Проценты: ({percent_x:.1f}%, {percent_y:.1f}%)")
    print(f"  Для кода: click_relative(driver, {percent_x:.1f}, {percent_y:.1f})")