import signal
import sys

from dotenv import load_dotenv
from google.cloud import speech

from audio import MicrophoneStream
from manager import listen_loop

load_dotenv()

# audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)


def cleanup(*args):
    print("exit")
    sys.exit(0)


signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGTSTP, cleanup)

# See http://g.co/cloud/speech/docs/languages
# for a list of supported languages.
language_code = "tr-TR"

client = speech.SpeechClient()
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=RATE,
    language_code=language_code,
)

streaming_config = speech.StreamingRecognitionConfig(
    config=config, interim_results=True
)

with MicrophoneStream(RATE, CHUNK) as stream:
    audio_generator = stream.generator()
    requests = (
        speech.StreamingRecognizeRequest(audio_content=content)
        for content in audio_generator
    )

    print("Listening..")
    responses = client.streaming_recognize(streaming_config, requests)

    # now, put the transcription responses to use.
    listen_loop(responses)
