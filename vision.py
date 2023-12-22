import base64
import json
import os
from io import BytesIO

import openai
import instructor
from dotenv import load_dotenv
from PIL import Image
from openai import OpenAI
from pydantic import BaseModel
from typing import Optional
from instructor import Mode

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
IMG_RES = 1080

# Enables `response_model`
client = instructor.patch(OpenAI(), mode=instructor.function_calls.Mode.MD_JSON)


# Function to encode the image
def encode_and_resize(image):
    W, H = image.size
    image = image.resize((IMG_RES, int(IMG_RES * H / W)))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return encoded_image

class action_details(BaseModel):
    
    action: str
    character_string: str
    confidence: str
    type_input : Optional[str]
    url : Optional[str]
    done : Optional[None]


def get_actions(screenshot, objective, previous_action):
    encoded_screenshot = encode_and_resize(screenshot)
    example_json = '''
        {
            'action': 'character sequence',
            'character_string': str
            'type input': str
            url: str # optional
            'done': None #optional
        }
    '''
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        response_model=action_details,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""You are a web navigator who needs to choose which action to take to achieve objective: {objective}. Your last action was: {previous_action}. 
                        Considering your overall objective, the current state of the browser page, select your next step. 
                        Your action options are navigate, type, click, and done. 
                        If you select navigatge, you must specify a URL. 
                        If you select type or string, you must specify the yellow character sequence you want to click on, and to type you must specify the input to type. 
                        For clicks, please only specify with the 1-2 letter sequence in the yellow box, and if there are multiple valid options choose the one you think a user would select. 
                        For typing, please specify a click to click on the box along with a type with the message to write. 
                        When the page seems satisfactory, return done as a key with no value. 
                        You must specify a level of confidence that your decision will further the objective. Please think closely about this, as there are alternatives if you are not confident. 
                        The value of the confidence key must be one of LOW, MEDIUM, HIGH scoring of your confidence that your action is correct.

                                The outputted JSON MUST look like:
                                {example_json}
                        """,
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
        max_tokens=200,
    )

    print(response)
    return response


if __name__ == "__main__":
    image = Image.open("image.png")
    actions = get_actions(image, "upvote the pinterest post")


