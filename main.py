import vision
from vimbot import Vimbot


def main():
    # Prompt the user for their intent
    objective = input("Please enter your objective: ")

    driver = Vimbot()
    driver.go_to_page("https://www.google.com")
    while True:
        screenshot_filename = driver.capture()
        actions = vision.get_actions(screenshot_filename, objective)
        driver.perform_actions(actions)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        exit()
