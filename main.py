import time

import vision
from vimbot import Vimbot, get_chrome_user_data_dir


def main():
    print("Initializing the Vimbot driver...")
    user_data_dir = get_chrome_user_data_dir()
    driver = Vimbot(user_data_dir=user_data_dir)

    print("Navigating to Google...")
    driver.navigate("https://www.google.com")

    objective = input("Please enter your objective: ")
    while True:
        time.sleep(1)
        print("Capturing the screen...")
        screenshot = driver.capture()

        print("Getting actions for the given objective...")
        action = vision.get_actions(screenshot, objective)
        print(f"JSON Response: {action}")
        if driver.perform_action(action):  # returns True if done
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
