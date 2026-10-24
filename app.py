from elevenlabs import ElevenLabs
from elevenlabs.play import play
from dotenv import load_dotenv
load_dotenv()

client = ElevenLabs()

audio = client.text_to_speech.convert(
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    output_format="mp3_44100_128",
    text="The first move is what sets everything in motion.",
    model_id="eleven_multilingual_v2",)
play(audio=audio)