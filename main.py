import os
import time

import openai
from dotenv import load_dotenv

from vimbot import Vimbot
from vision import step

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_page_data(driver, url, user_intent, actions_folder="screenshots"):
    driver.get(url)
    time.sleep(3)  # Adjust time as necessary to ensure the page loads

    # Save screenshot to the specified folder
    screenshot_path = os.path.join(actions_folder, "screenshot.png")
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")

    # Here you would call the real GPT API and get the actions
    # For now, we'll use a mock response based on the user's intent
    # actions = step(user_intent)

    # Perform actions as instructed by the GPT response
    # perform_actions(driver, actions)

    return screenshot_path


def main():
    # Prompt the user for their intent
    user_objective = input("Please enter your objective: ")

    driver = Vimbot()
    driver.go_to_page("https://www.google.com")
    driver.capture("screenshot.png")

    # screenshot, html_source = get_page_data(driver, url, user_intent)

    driver.quit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        exit()
