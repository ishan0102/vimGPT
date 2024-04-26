import base64
import json
from io import BytesIO
import openai
from dotenv import load_dotenv
from PIL import Image
import requests
import replicate
import ast
import anthropic

load_dotenv()
IMG_RES = 1080

# Function to encode the image
def encode_and_resize(image):
    W, H = image.size
    image = image.resize((IMG_RES, int(IMG_RES * H / W)))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return encoded_image

def get_actions(screenshot, objective, model):
    encoded_screenshot = encode_and_resize(screenshot)
    if model == 'claude': # Anthropic API
        message = anthropic.Anthropic().messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": encoded_screenshot,
                        }
                    },
                    {
                        "type": "text",
                        "text": f"You need to choose which action to take to help a user do this task: {objective}. Your options are navigate, type, click, and done. Navigate should take you to the specified URL. Type and click take strings where if you want to click on an object, return the string with the yellow character sequence you want to click on, and to type just a string with the message you want to type. For clicks, please only respond with the 1-2 letter sequence in the yellow box, and if there are multiple valid options choose the one you think a user would select. For typing, please return a click to click on the box along with a type with the message to write. When the page seems satisfactory, return done as a key with no value. You must respond in JSON only with no other fluff or bad things will happen. The JSON keys must ONLY be one of navigate, type, or click. Do not return the JSON inside a code block. Your answer needs to be in this dictionary format: 'click': 'D', 'type': 'rick roll'. This is the correct response if you want to click on the yellow box D and type 'rick roll'. Please do this correctly, don't include key-value pairs if the value is empty. The 'click' key value pair must be a yellow box you can see in the screenshot. Do not return an empty string as a value to a key. Do not include the key-value pair of 'done' unless you believe the objective has been completed. If you want to click on something, PLEASE analyze the image and make sure the field you want to click on exists as a yellow highlighted box."
                    }
                ]
            }
        ]
        )
        return json.loads(message.content[0].text)
    if model == 'llava': # Ollama Local API
        url = 'http://localhost:11434/api/generate'
        data = {
            'model': 'llava',
            'prompt': f"You need to choose which action to take to help a user do this task: {objective}. Your options are navigate, type, click, and done. Navigate should take you to the specified URL. Type and click take strings where if you want to click on an object, return the string with the yellow character sequence you want to click on, and to type just a string with the message you want to type. For clicks, please only respond with the 1-2 letter sequence in the yellow box, and if there are multiple valid options choose the one you think a user would select. For typing, please return a click to click on the box along with a type with the message to write. When the page seems satisfactory, return done as a key with no value. You must respond in JSON only with no other fluff or bad things will happen. The JSON keys must ONLY be one of navigate, type, or click. Do not return the JSON inside a code block. Your answer needs to be in this dictionary format: 'click': 'D', 'type': 'rick roll'. This is the correct response if you want to click on the yellow box D and type 'rick roll'. Please do this correctly, don't include key-value pairs if the value is empty. The 'click' key value pair must be a yellow box you can see in the screenshot. Do not return an empty string as a value to a key. Do not include the key-value pair of 'done' unless you believe the objective has been completed. If you want to click on something, PLEASE analyze the image and make sure the field you want to click on exists as a yellow highlighted box.",
            'images': [encoded_screenshot],
            'format': 'json'
        }
        response = requests.post(url, json=data)
        jsonStrings = response.text.split('\n') 
        output = ''
        for i in jsonStrings:
            if i.strip():
                real = json.loads(i)
                output += real['response']
        return json.loads(output)
    if model == 'cogvlm': # NEEDS WORK, Replicate API
        output = replicate.run("naklecha/cogvlm:ec3886f9ea85dd0aee216585be5e6d07b04c9650f7b8b08363a14eb89e207eb2",
        input={
            "image": f"data:image/jpeg;base64,{encoded_screenshot}",
            "prompt": f"You need to choose which action to take to help a user do this task: {objective}. Your options are navigate, type, click, and done. Navigate should take you to a specified URL. Type and click take strings where if you want to click on an object, return the string with the yellow character sequence you want to click on, and to type just a string with the message you want to type. For clicks, please only respond with the 1-2 letter sequence in the yellow box, and if there are multiple valid options choose the one you think a user would select. For typing, please return a click to click on the box along with a type with the message to write. When the page seems satisfactory, return done as a key with no value. You must respond in JSON only with no other fluff or bad things will happen. The JSON keys must ONLY be one of navigate, type, or click. Do not return the JSON inside a code block. Your answer needs to be in this dictionary format: 'click': 'D', 'type': 'rick roll'. This is the correct response if you want to click on the yellow box D and type 'rick roll'. Please do this correctly, don't include key-value pairs if the value is empty. The 'click' key value pair must be a yellow box you can see in the screenshot. Do not return an empty string as a value to a key. Do not include the key-value pair of 'done' unless you believe the objective has been completed. If you want to click on something, PLEASE analyze the image and make sure the field you want to click on exists as a yellow highlighted box. If you want to navigate, you must provide a link as the value to the key-value pair of navigate. YOU MUST RESPOND IN DICTIONARY FORMAT, WRAP YOUR ANSWERS WITH {{}} CHARACTERS PLEASE."
        }
        )
        print(output)
        formatted_string = "{'" + output.replace(": ", "': ").replace(", ", ", '") + "}" # This does not always transform the output to a dictionary
        dictionary = ast.literal_eval(formatted_string)
        newJson = json.dumps(dictionary, indent=4)
        return json.loads(newJson)
    if model == 'gpt4v': #OpenAI API
        response = openai.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"You need to choose which action to take to help a user do this task: {objective}. Your options are navigate, type, click, and done. Navigate should take you to the specified URL. Type and click take strings where if you want to click on an object, return the string with the yellow character sequence you want to click on, and to type just a string with the message you want to type. For clicks, please only respond with the 1-2 letter sequence in the yellow box, and if there are multiple valid options choose the one you think a user would select. For typing, please return a click to click on the box along with a type with the message to write. When the page seems satisfactory, return done as a key with no value. You must respond in JSON only with no other fluff or bad things will happen. The JSON keys must ONLY be one of navigate, type, or click. Do not return the JSON inside a code block.",
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
        try:
            json_response = json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            print("Error: Invalid JSON response")
            cleaned_response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant to fix an invalid JSON response. You need to fix the invalid JSON response to be valid JSON. You must respond in JSON only with no other fluff or bad things will happen. Do not return the JSON inside a code block.",
                    },
                    {"role": "user", "content": f"The invalid JSON response is: {response.choices[0].message.content}"},
                ],
            )
            try:
                cleaned_json_response = json.loads(cleaned_response.choices[0].message.content)
            except json.JSONDecodeError:
                print("Error: Invalid JSON response")
                return {}
            return cleaned_json_response
        return json_response
    return None

if __name__ == "__main__":
    image = Image.open("image.png")
    actions = get_actions(image, "upvote the pinterest post")
