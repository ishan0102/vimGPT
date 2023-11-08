import vision
from vimbot import Vimbot


def main():
    driver = Vimbot()
    driver.navigate("https://www.google.com")
    while True:
        objective = input("Please enter your objective: ")
        screenshot = driver.capture()
        action = vision.get_actions(screenshot, objective)
        driver.perform_action(action)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        exit()
