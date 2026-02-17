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

time.sleep(5)
driver.quit()