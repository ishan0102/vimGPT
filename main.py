import os
import time

import openai
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from vision import step

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def setup_driver():
    options = Options()
    options.headless = True
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    return driver


def perform_actions(driver, actions):
    wait = WebDriverWait(driver, 10)
    for action in actions:
        if action["action"] == "click":
            # Click an element with a CSS selector
            element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, action["css_selector"])))
            element.click()
            print(f"Clicked on element with selector: {action['css_selector']}")
        elif action["action"] == "type":
            # Type text into an input field with a CSS selector
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, action["css_selector"])))
            element.send_keys(action["text"])
            print(f"Typed '{action['text']}' into element with selector: {action['css_selector']}")
        elif action["action"] == "navigate":
            driver.get(action["url"])
            print(f"Navigated to {action['url']}")


def get_page_data(driver, url, user_intent, actions_folder="screenshots"):
    driver.get(url)
    time.sleep(3)  # Adjust time as necessary to ensure the page loads

    # Save screenshot to the specified folder
    screenshot_path = os.path.join(actions_folder, "screenshot.png")
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")

    # Get the HTML source
    html_source = driver.page_source
    print(html_source)

    # Here you would call the real GPT API and get the actions
    # For now, we'll use a mock response based on the user's intent
    # actions = step(user_intent)

    # Perform actions as instructed by the GPT response
    # perform_actions(driver, actions)

    return screenshot_path, html_source


def main():
    driver = setup_driver()

    # Prompt the user for their intent
    user_intent = input("Please enter your intent: ")

    # For demonstration, the URL is static. You would dynamically set this based on the intent
    url = "http://google.com"

    screenshot, html_source = get_page_data(driver, url, user_intent)
    print(html_source)  # Optionally print the HTML source of the page

    # Clean up: close the browser window
    driver.quit()


if __name__ == "__main__":
    main()
