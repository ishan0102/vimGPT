import base64
import os

import openai
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class Action(BaseModel):
    navigate: str = None
    type: str = None
    click: str = None
    complete: bool = False


class Actions(BaseModel):
    actions: list[Action]


# Function to encode the image
def encode_and_resize(filename, width):
    with open(os.path.join("screenshots", filename), "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_actions(screenshot_filename, objective):
    encoded_screenshot = encode_and_resize(screenshot_filename)
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "You are shown a browser screenshot with yellow symbols indicating the locations of clickable items. What is the character sequence of the symbol that would allow us to {objective}?}",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_screenshot}",
                        },
                    },
                ],
            }
        ],
        max_tokens=100,
    )

    print(response.choices[0])


def get_actions_mock(encoded_screenshot):
    return [
        {
            "type": "text",
            "text": "What’s in this image?",
        },
        {
            "type": "image_url",
            "image_url": f"data:image/jpeg;base64,{encoded_screenshot}",
        },
        {
            "type": "text",
            "text": "It's a picture of a cat.",
        },
    ]


if __name__ == "__main__":
    get_actions("image.png", "go to engblogs github")
