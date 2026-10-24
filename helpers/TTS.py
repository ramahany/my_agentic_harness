from elevenlabs import ElevenLabs
from elevenlabs.play import play
from dotenv import load_dotenv
load_dotenv()

class TTS(): 
    def __init__(self):
        self.client = ElevenLabs()

    def play_audio_from_text(self, text:str): 
        audio = self.client.text_to_speech.convert(
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            output_format="mp3_44100_128",
            text=text,
            model_id="eleven_multilingual_v2",)
        play(audio=audio)