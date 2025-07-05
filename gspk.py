import readline
import requests
from gtts import gTTS
import subprocess
import os

OLLAMA_API_URL = "http://localhost:11434/api/chat"
MODEL = "llama3:8b"
AUDIO_FILE = "output.mp3"

def speak_loop():
    print("Enter prompt for Ollama (type 'exit' to quit):")
    while True:
        user_input = input(">>> ",)
        if user_input.strip().lower() == "exit":
            print("Exiting...")
            break

        try:
            # Prepare Ollama API payload
            payload = {
                "model": MODEL,
                "stream": False,
                "messages": [
                    {"role": "user", "content": f"{user_input.strip()} Please respond in the shortest and most concise way you can."}
                ]
            }

            # Send request to Ollama
            response = requests.post(OLLAMA_API_URL, json=payload)
            response.raise_for_status()
            content = response.json()["message"]["content"]
            print(f"Ollama: {content}")

            # Convert text to speech using gTTS
            tts = gTTS(text=content, lang='en', slow=False)
            tts.save(AUDIO_FILE)

            # Play the audio using mpg321
            subprocess.run(["mpg321", AUDIO_FILE], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Optional: delete the file afterward
            os.remove(AUDIO_FILE)

        except requests.exceptions.RequestException as e:
            print(f"API error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

# Run the loop
speak_loop()

