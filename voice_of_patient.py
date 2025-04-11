import logging
import os
import subprocess
import time
import speech_recognition as sr

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Step 1: Record only if user starts speaking within 5 seconds
def record_audio_wav(temp_wav_path="temp_patient_audio.wav", wait_for_speech=5):
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            logging.info("Listening for your voice... Speak within 5 seconds or recording will stop.")

            recognizer.adjust_for_ambient_noise(source, duration=1)

            try:
                audio_data = recognizer.listen(source, timeout=wait_for_speech, phrase_time_limit=10)
                with open(temp_wav_path, "wb") as f:
                    f.write(audio_data.get_wav_data())
                logging.info(f"Audio recorded and saved to {temp_wav_path}")
                return True  # Recording succeeded

            except sr.WaitTimeoutError:
                logging.warning("No speech detected within the wait time. Stopping.")
                return False  # No speech

    except Exception as e:
        logging.error(f"An error occurred during recording: {e}")
        return False

# Step 2: Convert WAV to MP3 using ffmpeg
def convert_wav_to_mp3(input_wav_path, output_mp3_path):
    try:
        command = [
            "ffmpeg",
            "-y",
            "-i", input_wav_path,
            "-vn",
            "-ar", "44100",
            "-ac", "1",
            "-b:a", "128k",
            output_mp3_path
        ]
        subprocess.run(command, check=True)
        logging.info(f"Converted {input_wav_path} to {output_mp3_path} using FFmpeg")
    except subprocess.CalledProcessError as e:
        logging.error(f"FFmpeg error: {e}")

# Step 3: Transcribe using Groq STT
def transcribe_with_groq(stt_model, audio_filepath, groq_api_key):
    from groq import Groq
    client = Groq(api_key=groq_api_key)

    with open(audio_filepath, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=stt_model,
            file=audio_file,
            language="en"
        )
    return transcription.text

# ===== Main Execution =====
if __name__ == "__main__":
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    stt_model = "whisper-large-v3"

    # File paths
    wav_path = "temp_patient_audio.wav"
    mp3_path = "patient_voice_test_for_patient.mp3"

    # Start recording
    recorded = record_audio_wav(temp_wav_path=wav_path, wait_for_speech=5)

    if recorded:
        convert_wav_to_mp3(input_wav_path=wav_path, output_mp3_path=mp3_path)
        transcription_text = transcribe_with_groq(stt_model, mp3_path, GROQ_API_KEY)

        print("\n--- Transcription Output ---")
        print(transcription_text)
    else:
        print("\n⚠️ No speech detected. Try again.")
