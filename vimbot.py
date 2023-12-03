import os
import platform
import time
from io import BytesIO

from PIL import Image
from playwright.sync_api import sync_playwright

vimium_path = "./vimium-master"


class Vimbot:
    def __init__(self, headless=False, user_data_dir=None):
        playwright = sync_playwright().start()
        browser_args = [
            f"--disable-extensions-except={vimium_path}",
            f"--load-extension={vimium_path}"
        ]
        self.context = playwright.chromium.launch_persistent_context(
            user_data_dir,  # Specify the user data directory here
            headless=headless,
            args=browser_args,
            ignore_https_errors=True
        )
        self.page = self.context.new_page()
        self.page.set_viewport_size({"width": 1080, "height": 720})

    def perform_action(self, action):
        if "done" in action:
            return True
        if "click" in action and "type" in action:
            self.click(action["click"])
            self.type(action["type"])
        if "navigate" in action:
            self.navigate(action["navigate"])
        elif "type" in action:
            self.type(action["type"])
        elif "click" in action:
            self.click(action["click"])

    def navigate(self, url):
        self.page.goto(url=url if "://" in url else "https://" + url, timeout=60000)

    def type(self, text):
        time.sleep(1)
        self.page.keyboard.type(text)
        self.page.keyboard.press("Enter")

    def click(self, text):
        self.page.keyboard.type(text)

    def capture(self):
        # capture a screenshot with vim bindings on the screen
        self.page.keyboard.press("Escape")
        self.page.keyboard.type("f")

        screenshot = Image.open(BytesIO(self.page.screenshot())).convert("RGB")
        return screenshot


def get_chrome_user_data_dir():
    system = platform.system()

    if system == "Windows":
        base_path = os.path.join(os.environ['USERPROFILE'], "AppData", "Local", "Google", "Chrome", "User Data")
    elif system == "Darwin":
        base_path = os.path.join(os.path.expanduser('~'), "Library", "Application Support", "Google", "Chrome")
    elif system == "Linux":
        base_path = os.path.join(os.path.expanduser('~'), ".config", "google-chrome")

    if os.path.exists(base_path):
        return base_path
    else:
        print('User data dir not found')
        return None
