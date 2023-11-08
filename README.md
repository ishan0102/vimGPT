# vimGPT
Giving multimodal models an interface to play with.

https://github.com/ishan0102/vimGPT/assets/47067154/467be2ac-7e8d-47de-af89-5bb6f51c1c31

## Overview
LLMs as a way to browse the web is being explored by numerous startups and open-source projects. With this project, I was interested in seeing if we could only use [GPT-4V](https://openai.com/research/gpt-4v-system-card)'s vision capabilities for web browsing.

The issue with this is it's hard to determine what the model wants to click on without giving it the browser DOM as text. [Vimium](https://vimium.github.io/) is a Chrome extension that lets you navigate the web with only your keyboard. I thought it would be interesting to see if we could use Vimium to give the model a way to interact with the web.

## Setup
Install Python requirements
```
pip install -r requirements.txt
```

Download Vimium locally (have to load the extension manually when running Playwright)
```
./setup.sh
```

## References
- https://github.com/Globe-Engineer/globot
- https://github.com/nat/natbot
