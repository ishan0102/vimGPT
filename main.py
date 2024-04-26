import argparse
import time
from whisper_mic import WhisperMic
import vision
from vimbot import Vimbot

def main(voice_mode):
    print("Initializing the Vimbot driver...")
    driver = Vimbot()

    print("Navigating to Google...")
    driver.navigate("https://www.google.com")

    if voice_mode:
        print("Voice mode enabled. Listening for your command...")
        mic = WhisperMic()
        try:
            objective = mic.listen()
        except Exception as e:
            print(f"Error in capturing voice input: {e}")
            return  # Exit if voice input fails
        print(f"Objective received: {objective}")
    else:
        objective = input("Please enter your objective: ")
        model = input("Please enter a model to use (llava, gpt4v, cogvlm, claude): ")

    while True:
        time.sleep(1)
        print("Capturing the screen...")
        screenshot = driver.capture()
        print("Getting actions for the given objective...")
        action = vision.get_actions(screenshot, objective, model)
        print(f"JSON Response: {action}")
        if driver.perform_action(action):  # returns True if done
            break

def main_entry():
    parser = argparse.ArgumentParser(description="Run the Vimbot with optional voice input.")
    parser.add_argument(
        "--voice",
        help="Enable voice input mode",
        action="store_true",
    )
    args = parser.parse_args()
    main(args.voice)

if __name__ == "__main__":
    try:
        main_entry()
    except KeyboardInterrupt:
        print("Exiting...")
