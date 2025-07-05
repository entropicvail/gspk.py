# Overview

This script uses ollama and the Google Translate Text-to-Speech to create an on-prem (no network required) ability to have text to speach interactions with an LLM. There is nothing really ground-breaking going on, just a nicer way to interact with an LLM sometimes. Next, I will work on creating a bridge for ollama to interface with a local data-set (like Obsidian notes) to consider during interaction.

## Requirements

This is designed to run in a Python venv. Create a dir called spk and copy in gspk.py; cd into spk, then run the following to set up the environment:

```
python -m venv venv
```

**Install Dependencies**

```
curl -fsSL https://ollama.com/install.sh | sh
```
```
ollama pull llama3:8b
```
```
sudo apt update && sudo apt install mpg321 -y
``````
source ./venv/bin/activate
```
```
pip install gTTS
```

**Run the program**

Ensure ollama is running in the background by:
```
ollama serve &
```
**OR**
```
sudo systemctl start ollama.service
```

From inside your venv, run the program by:
```
python gpsk.py
```

Your prompts into the python environment will be sent to ollama for interpolation, the response will be fed out into an audio file that is automatically played back. The audio file is deleated automatically, but you can comment the corosponding segment out in gspk.py to retain them if desired.
