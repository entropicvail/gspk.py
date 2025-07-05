import readline
import requests
import subprocess
import os
import time

OLLAMA_API_URL = "http://localhost:11434/api/chat"
MODEL = "llama3:8b"
OPENTTS_URL = "http://localhost:5500/api/tts"
AUDIO_FILE = "output.wav"
VOICE = "larynx:en-us_mary_ann-glow_tts"  # change to another supported OpenTTS voice if desired

def start_opentts_docker():
    # Check if container is already running
    check_cmd = ["sudo", "docker", "ps", "--filter", "ancestor=synesthesiam/opentts", "--format", "{{.ID}}"]
    result = subprocess.run(check_cmd, capture_output=True, text=True)
    
    if result.stdout.strip():
        print("OpenTTS container is already running.")
        return
    
    print("Starting OpenTTS Docker container...")
    
    try:
        # Run the container in detached mode
        subprocess.run([
            "sudo", "docker", "run", "-d", "-p", "5500:5500", "--name", "opentts", "synesthesiam/opentts"
        ], check=True)
        
        # Wait a moment for the server to start
        print("Waiting for OpenTTS to initialize...")
        time.sleep(5)
    
    except subprocess.CalledProcessError as e:
        print("Failed to start OpenTTS Docker container.")
        print(e)
        exit(1)

def stop_opentts_docker():
    print("Stopping OpenTTS Docker container...")
    try:
        subprocess.run(["sudo", "docker", "stop", "opentts"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["sudo", "docker", "rm", "opentts"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("OpenTTS container stopped and removed.")
    except subprocess.CalledProcessError:
        print("Could not stop/remove OpenTTS container. It may not have been running.")

def speak_loop():
    start_opentts_docker()
    print("Enter prompt for Ollama (type 'exit' to quit):")
    while True:
        try:
            user_input = input(">>> ")
            if user_input.strip().lower() == "exit":
                print("Exiting...")
                stop_opentts_docker()
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
