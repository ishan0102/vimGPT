import vision
from vimbot import Vimbot


def main():
    driver = Vimbot()
    driver.go_to_page("https://www.google.com")
    while True:
        objective = input("Please enter your objective: ")
        screenshot = driver.capture()
        action = vision.get_actions(screenshot, objective)
        driver.perform_actions(action)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        exit()
