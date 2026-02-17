import unittest
import pytest

from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    appPackage='com.android.settings',
    appActivity='.Settings',
    language='en',
    locale='US'
)

appium_server_url = 'http://localhost:4723'

@pytest.fixture()
def driver():
    android_driver = webdriver.Remote(appium_server_url, capabilities)
    yield android_driver
    if android_driver:
        android_driver.quit()

def test_find_battery(self) -> None:
    el = self.driver.find_element(by=AppiumBy.XPATH, value='//*[@text="Battery"]')
    el.click()