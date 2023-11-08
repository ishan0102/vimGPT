from io import BytesIO

from PIL import Image
from playwright.sync_api import sync_playwright

vimium_path = "./vimium-master"


class Vimbot:
    def __init__(self, headless=False):
        print("Starting Vimbot...")
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
        self.page.set_viewport_size({"width": 1280, "height": 1080})

    def perform_actions(self, actions):
        # actions is a piece of json from the openai api
        for action in actions:
            if action["type"] == "text":
                self.type(action["text"], submit=True)
            elif action["type"] == "key":
                self.page.keyboard.press(action["key"])
            elif action["type"] == "click":
                self.page.click(action["selector"])

    def navigate(self, url):
        self.page.goto(url=url if "://" in url else "https://" + url, timeout=60000)

    def type(self, text):
        self.page.keyboard.type(text)
        self.page.keyboard.press("Enter")

    def click(self, text):
        self.page.type(text)

    def capture(self):
        # capture a screenshot with vim bindings on the screen
        self.page.keyboard.press("Escape")
        self.page.keyboard.type("f")

        screenshot = Image.open(BytesIO(self.page.screenshot())).convert("RGB")
        return screenshot
