import base64

from playwright.sync_api import sync_playwright


class Bot:
    def __init__(self, headless=False):
        self.browser = sync_playwright().start().chromium.launch(headless=headless)

        self.context = self.browser.new_context(
            # Uncomment if you start getting blocked
            # user_agent=UserAgent().random,
            ignore_https_errors=True,
        )
        self.page = self.context.new_page()
        self.page.set_viewport_size({"width": 1280, "height": 1080})

    def go_to_page(self, url):
        self.page.goto(url=url if "://" in url else "https://" + url, timeout=60000)
        self.client = self.page.context.new_cdp_session(self.page)

    def type(self, text, submit=False):
        self.page.keyboard.type(text)
        if submit:
            self.page.keyboard.press("Enter")

    def capture(self, path):
        screenshot = self.page.screenshot()
        encoded = base64.b64encode(screenshot).decode("utf-8")
        return encoded
