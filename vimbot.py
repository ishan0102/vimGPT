import base64

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

    def go_to_page(self, url):
        self.page.goto(url=url if "://" in url else "https://" + url, timeout=60000)

    def type(self, text, submit=False):
        self.page.keyboard.type(text)
        if submit:
            self.page.keyboard.press("Enter")

    def capture(self, path):
        # capture a screenshot with vim bindings on the screen
        self.page.keyboard.press("Escape")
        self.page.keyboard.type("f")

        screenshot = self.page.screenshot()
        with open(path, "wb") as f:
            f.write(screenshot)
        encoded = base64.b64encode(screenshot).decode("utf-8")
        return encoded
