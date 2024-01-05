import time
from io import BytesIO

from PIL import Image
from playwright.sync_api import sync_playwright
import re


vimium_path = "./vimium-master"


class Vimbot:
    def __init__(self, headless=False):
        self.context = (
            sync_playwright()
            .start()
            .chromium.launch_persistent_context(
                "",
                headless=headless,
                args=[
                    f"--disable-extensions-except={vimium_path}",
                    f"--load-extension={vimium_path}",
                ],
                ignore_https_errors=True,
            )
        )

        self.page = self.context.new_page()
        self.page.set_viewport_size({"width": 1080, "height": 720})

    

    def perform_action(self, action):
        if "done" in action.action:
            return True
        if  "type" in action.action:
            self.click(action.character_string)
            self.type(action.type_input)
        if "navigate" in action.action :
            self.navigate(action.url)
        elif "click" in action.action:
            self.click(action.character_string)

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


