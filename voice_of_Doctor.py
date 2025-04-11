# from gtts import gTTS
# from playsound import playsound

# def text_to_speech_with_gtts(input_text, output_filepath):
#     tts = gTTS(text=input_text, lang='en', slow=False)
#     tts.save(output_filepath)
#     playsound(output_filepath)

# input_text = "Hello this skintel AI. tell me your any dermo particular query and i will help you with that."
# text_to_speech_with_gtts(input_text, "gtts_testing_autoplay.mp3")

from gtts import gTTS
from playsound import playsound

def speak_text_with_gtts(input_text: str, output_filepath: str = "doctor_response.mp3"):
    """
    Convert text to speech using gTTS and play the audio.

    Args:
        input_text (str): Text to convert into speech.
        output_filepath (str): Path to save the mp3 audio file.
    """
    tts = gTTS(text=input_text, lang='en', slow=False)
    tts.save(output_filepath)
    playsound(output_filepath)
