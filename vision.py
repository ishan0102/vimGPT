import base64
import json
import os
from io import BytesIO

import openai
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
IMG_RES = 1080


# Function to encode the image
def encode_and_resize(image):
    W, H = image.size
    image = image.resize((IMG_RES, int(IMG_RES * H / W)))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return encoded_image


def get_actions(screenshot, objective):
    encoded_screenshot = encode_and_resize(screenshot)
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"You need to choose which action to take to help a user do this task: {objective}. Your options are navigate, type, and click. Navigate should take you to the specified URL. Type and click take strings where if you want to click on an object, return the string with the yellow character sequence you want to click on, and to type just a string with the message you want to type. You must respond in JSON only with no other fluff or bad things will happen. The JSON keys must ONLY be one of navigate, type, or click. Do not return the JSON inside a code block.",
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

    json_response = json.loads(response.choices[0]["message"]["content"])
    print(f"JSON Response: {json_response}")
    return json_response


if __name__ == "__main__":
    image = Image.open("image.png")
    actions = get_actions(image, "upvote the pinterest post")
