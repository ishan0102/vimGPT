# vimGPT
Giving multimodal models an interface to play with.

https://github.com/ishan0102/vimGPT/assets/47067154/467be2ac-7e8d-47de-af89-5bb6f51c1c31

## Overview
LLMs as a way to browse the web is being explored by numerous startups and open-source projects. With this project, I was interested in seeing if we could only use [GPT-4V](https://openai.com/research/gpt-4v-system-card)'s vision capabilities for web browsing.

The issue with this is it's hard to determine what the model wants to click on without giving it the browser DOM as text. [Vimium](https://vimium.github.io/) is a Chrome extension that lets you navigate the web with only your keyboard. I thought it would be interesting to see if we could use Vimium to give the model a way to interact with the web.

## Usage
Install Python requirements:
```
pip install -r requirements.txt
```

Download Vimium locally (have to load the extension manually when running Playwright):
```
./setup.sh
```

Run the script:
```
python main.py
```

## Voice Mode
Voice Mode: Engage with the browser using voice commands. Simply say your objective, and watch vimGPT perform actions in real-time.
```
python main.py --voice
```

## Ideas
Feel free to collaborate with me on this, I have a number of ideas:
- Use [Assistant API](https://platform.openai.com/docs/assistants/overview) once it's released for automatic context retrieval. The Assistant API will create a thread that we can add messages too, to keep the history of actions, but it doesn't support the Vision API yet.
- Vimium fork for overlaying elements. A specialized version of Vimium that selectively overlays elements based on context could be useful, effectively pruning based on the user query. Might be worth testing if different sized boxes/colors help.
- Use higher resolution images, as it seems to fail at low res. I noticed that below a certain threshold, the model wouldn't detect anything. This might be improved by using higher resolution images but that would require more tokens.
- Fine-tune [LLaVa](https://github.com/haotian-liu/LLaVA) or [CogVLM](https://github.com/THUDM/CogVLM) to do this or [Fuyu-8B](https://www.adept.ai/blog/fuyu-8b). Could be faster/cheaper. CogVLM can accurately specify pixel coordinates which may be a good way to augment this.
- Use JSON mode once it's released for Vision API. Currently the Vision API doesn't support JSON mode or function calling, so we have to rely on more primitive prompting methods.
- Have the Vision API return general instructions, formalized by another call to the JSON mode version of the API. This is a workaround for the JSON mode issue but requires another LLM call, which is slower/more expensive.
- Add speech-to-text with Whisper or another model to eliminate text input and make this more accessible.
- Make this work for your own browser instead of spinning up an artificial one. I want to be able to order food with my credit card.
- Provide the frames with and without Vimium enabled in case the model can't see what's under the yellow square.
- Pass the Chrome accessibility tree in as input in addition to the image. This provides a layout of interactive elements that can be mapped to the Vimium bindings.
- Have it write longer things based on the context of the page or return information to the user based on the query. Examples are replying to an email, summarizing a news article, etc. Visual question answering.
- Make this a useful tool for blind people by adding voice mode and a key that creates an Assistant API for a given page. Something where you can "speak to an agent" about a page content in natural language.
- Use Javascript to label DOM elements with colored boxes, similar to [this](https://x.com/DivGarg9/status/1659270501498523648?s=20).
- Build a graph-based retry mechanism that makes sure we aren't falling into cycles, i.e. recursively clicking on the same element.

## References
- https://github.com/Globe-Engineer/globot
- https://github.com/nat/natbot
