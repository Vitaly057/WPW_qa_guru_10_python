import os
import pytest
import allure
from selene import browser
from dotenv import load_dotenv
from utils import attach
from selenium import webdriver
from selenium.webdriver import ChromeOptions

DEFAULT_BROWSER_VERSION = "122.0"
DEFAULT_BROWSER_NAME = "chrome"


@allure.step('Select browser version')
def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default='chrome', help="Choose browser name.")
    parser.addoption('--browser_version', default='122.0',
                     help='Choose browser version. For Chrome: 120.0 or 121.0 or 124.0.')


@allure.step('Load env')
@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="function", autouse=True)
def setup_browser(request):
    with allure.step('Driver configuration strategy'):
        browser_name = request.config.getoption('--browser_name')
        browser_name = browser_name if browser_name != '' else DEFAULT_BROWSER_NAME
        browser_version = request.config.getoption('--browser_version')
        browser_version = browser_version if browser_version != '' else DEFAULT_BROWSER_VERSION
        with allure.step('Select Driver loading strategy'):
            if browser_name.lower() == 'chrome':
                driver_options = ChromeOptions()

        browser.config.base_url = "https://www.autodoc.ru/"
        browser.config.window_width = 1920
        browser.config.window_height = 1080


        selenoid_capabilities = {
            "browserName": browser_name,
            "browserVersion": browser_version,
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True
            }
        }

        driver_options.capabilities.update(selenoid_capabilities)
        login = os.getenv('LOGIN')
        password = os.getenv('PASSWORD')
        driver = webdriver.Remote(command_executor=f"https://{login}:{password}@selenoid.autotests.cloud/wd/hub",
            options=driver_options)

        browser.config.driver = driver

    yield

    with allure.step('Add screenshot'):
        attach.add_screenshot(browser)

    with allure.step('Add logs'):
        attach.add_logs(browser)

    with allure.step('Add html'):
        attach.add_html(browser)

    with allure.step('Add video'):
        attach.add_video(browser)

    with allure.step('Add log file'):
        attach.add_log_file()

    with allure.step('Close driver'):
        browser.quit()
