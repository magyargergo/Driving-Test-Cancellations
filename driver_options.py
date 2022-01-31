import locale
import os
import tempfile

from fake_useragent import UserAgent
from seleniumwire import webdriver

from utils import get_random_proxy, fix_exit_type_flag

current_path = str(
    os.path.dirname(os.path.realpath(__file__))
)  # Gets current file location
buster_path = f"{current_path}/buster-chrome.crx"


class DriverOptions(webdriver.ChromeOptions):
    def __init__(self, buster_enabled):

        super().__init__()

        self._arguments.append("--no-sandbox")
        self._arguments.append("--cryptauth-http-host ''")
        self._arguments.append("--disable-dev-shm-usage")
        self._arguments.append("--disable-accelerated-2d-canvas")
        self._arguments.append("--disable-blink-features=AutomationControlled")
        self._arguments.append("--disable-background-networking")
        self._arguments.append("--disable-background-timer-throttling")
        self._arguments.append("--disable-browser-side-navigation")
        self._arguments.append("--disable-client-side-phishing-detection")
        self._arguments.append("--disable-default-apps")
        self._arguments.append("--disable-device-discovery-notifications")
        self._arguments.append("--disable-extensions")
        self._arguments.append("--disable-features=site-per-process")
        self._arguments.append("--disable-hang-monitor")
        self._arguments.append("--disable-java")
        self._arguments.append("--disable-popup-blocking")
        self._arguments.append("--disable-prompt-on-repost")
        self._arguments.append("--disable-setuid-sandbox")
        self._arguments.append("--disable-sync")
        self._arguments.append("--disable-translate")
        self._arguments.append("--disable-web-security")
        self._arguments.append("--disable-webgl")
        self._arguments.append("--start-maximized")
        self._arguments.append("--metrics-recording-only")
        self._arguments.append("--no-first-run")
        self._arguments.append("--safebrowsing-disable-auto-update")
        self._arguments.append("--enable-automation")
        self._arguments.append("--password-store=basic")
        self._arguments.append("--use-mock-keychain")

        self._user_agent = UserAgent(verify_ssl=False).random
        self._arguments.append(f"--user-agent={self._user_agent}")

        # self._proxy = get_random_proxy()
        # self._arguments.append(f"--proxy-server={self._proxy}")

        user_data_dir = os.path.normpath(tempfile.mkdtemp())
        self._arguments.append(f"--user-data-dir={user_data_dir}")

        fix_exit_type_flag(user_data_dir)

        try:
            self._language = locale.getdefaultlocale()[0].replace("_", "-")
        except Exception:
            self._language = "en-US"

        self._arguments.append(f"--lang={self._language}")

        if buster_enabled:
            self._arguments.append(buster_path)

        self._experimental_options["useAutomationExtension"] = False
        self._experimental_options["excludeSwitches"] = ["enable-automation"]

    @property
    def user_agent(self):
        return self._user_agent

    @property
    def language(self):
        return self._language
