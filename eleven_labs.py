import requests
import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
from playsound import playsound


class ElevenVoice:

    def __init__(self):
        self.CHUNK_SIZE = 1024
        key = os.environ["ELEVEN_LABS_API"]
        self.headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": key
        }

    def generate_and_play_audio(self, content, voice_id):
        data = {
            "text": content,
            "model_id": "eleven_turbo_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        response = requests.post(url, json=data, headers=self.headers)
        with open('output.mp3', 'wb') as f:
            for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
                if chunk:
                    f.write(chunk)

        playsound('output.mp3')

if __name__ == "__main__":
    CELEBRITY_VOICE_ID_1 = os.environ["CELEBRITY_VOICE_ID_1"]
    voice = ElevenVoice()
    voice.generate_and_play_audio("Does this work?", CELEBRITY_VOICE_ID_1)