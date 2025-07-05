import readline
import requests
import subprocess
import os

OLLAMA_API_URL = "http://localhost:11434/api/chat"
MODEL = "llama3:8b"
OPENTTS_URL = "http://localhost:5500/api/tts"
AUDIO_FILE = "output.wav"
VOICE = "larynx:en-us_mary_ann-glow_tts"  # change to another supported OpenTTS voice if desired

def speak_loop():
    print("Enter prompt for Ollama (type 'exit' to quit):")
    while True:
        try:
            user_input = input(">>> ")
            if user_input.strip().lower() == "exit":
                print("Exiting...")
                break

            # Add concise instruction to the user message
            full_prompt = f"{user_input.strip()} Please respond in the shortest and most concise way you can."

            # Send prompt to Ollama
            payload = {
                "model": MODEL,
                "stream": False,
                "messages": [{"role": "user", "content": full_prompt}]
            }
            response = requests.post(OLLAMA_API_URL, json=payload)
            response.raise_for_status()
            content = response.json()["message"]["content"]
            print(f"\nOllama: {content}\n")

            # Request speech from OpenTTS
            tts_response = requests.get(OPENTTS_URL, params={"text": content, "voice": VOICE})
            if tts_response.status_code != 200:
                print(f"TTS Error: {tts_response.status_code}")
                continue

            # Save and play audio
            with open(AUDIO_FILE, "wb") as f:
                f.write(tts_response.content)

            subprocess.run(["aplay", AUDIO_FILE], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os.remove(AUDIO_FILE)

        except requests.exceptions.RequestException as e:
            print(f"API error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

# Run the interactive loop
speak_loop()

