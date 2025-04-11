# import os
# import gradio 


# from Brain_of_Bot import encode_image, analyze_image_with_query
# from voice_of_patient import record_audio_wav , convert_wav_to_mp3, transcribe_with_groq
# from voice_of_Doctor import speak_text_with_gtts

# speak_text_with_gtts(" your transcription goes here")

# from Brain_of_Bot import encode_image, analyze_image_with_query
# from voice_of_patient import record_audio_wav, convert_wav_to_mp3, transcribe_with_groq
# from voice_of_Doctor import speak_text_with_gtts


import gradio as gr
from Brain_of_Bot import encode_image, analyze_image_with_query
from voice_of_patient import record_audio_wav, convert_wav_to_mp3, transcribe_with_groq
from voice_of_Doctor import speak_text_with_gtts
import os

# Load environment variable
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
STT_MODEL = "whisper-large-v3"

# Function for full workflow
def skintel_ai_pipeline(image, user_input_audio):
    wav_path = "temp_patient_audio.wav"
    mp3_path = "patient_voice_test_for_patient.mp3"

    # Step 1: Record or use uploaded audio
    recorded = record_audio_wav(temp_wav_path=wav_path, wait_for_speech=5)
    if not recorded:
        return "⚠️ No voice detected. Try again.", None

    # Step 2: Convert to MP3
    convert_wav_to_mp3(input_wav_path=wav_path, output_mp3_path=mp3_path)

    # Step 3: Transcribe
    transcription_text = transcribe_with_groq(STT_MODEL, mp3_path, GROQ_API_KEY)

    # Step 4: Analyze image + transcription
    if image is not None:
        image_embedding = encode_image(image_path=image)
        analysis_response = analyze_image_with_query(transcription_text, encoded_image=image_embedding, model="llama3-8b-8192" ) 
    else:
        analysis_response = "No image provided. Please upload a skin image for analysis."

    # Step 5: Voice Response
    speak_text_with_gtts(analysis_response, "doctor_voice.mp3")

    return analysis_response, "doctor_voice.mp3"

# Gradio UI setup
iface = gr.Interface(
    fn=skintel_ai_pipeline,
    inputs=[
        gr.Image(type="filepath" , label="Upload Skin Image"),
        gr.Audio(sources=["microphone"], type="filepath", label="Speak Your Query")
    ],
    outputs=[
        gr.Textbox(label="Diagnosis / Response"),
        gr.Audio(label="Doctor Voice Response")
    ],
    title="🧠 Skintel AI - Skin Diagnosis Assistant",
    description="Upload a skin image and speak your query to get a diagnosis and voice feedback!"
)

if __name__ == "__main__":
    iface.launch()
