import vision
from vimbot import Vimbot


def main():
    print("Initializing the Vimbot driver...")
    driver = Vimbot()

    print("Navigating to Google...")
    driver.navigate("https://www.google.com")

    while True:
        objective = input("Please enter your objective: ")

        print("Capturing the screen...")
        screenshot = driver.capture()

        print("Getting actions for the given objective...")
        action = vision.get_actions(screenshot, objective)

        if action:
            print(f"Action determined: {action}")
            print("Performing the action...")
            driver.perform_action(action)
        else:
            print("No action could be determined.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
