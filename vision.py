import openai


def step(encoded_screenshot):
    # screenshot is a base64 encoded string
    response = openai.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image?"},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{encoded_screenshot}",
                    },
                ],
            }
        ],
        detail="low",
        max_tokens=300,
    )

    print(response.choices[0])
