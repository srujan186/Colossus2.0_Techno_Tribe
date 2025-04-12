
# 🩺 Skintel AI - Skin Diagnosis Assistant

A voice-enabled AI dermatology assistant that analyzes skin images and provides diagnoses via natural conversation. Built with Gradio, Groq API, and medical LLMs.

![Skintel Demo](demo-screenshot.jpg) *(Add a image of your skin problems here)*

## Features
- 🖼️ Upload skin images for visual analysis
- 🎙️ Voice-based symptom description
- 🤖 AI-powered diagnosis using Groq's `llama-3.2-90b-vision-preview`
- 🔊 Voice responses with gTTS
- 🚀 Real-time processing pipeline

## Installation

### Requirements
**Python 3.9+**  
**System Dependencies:**
- FFmpeg (for audio conversion)

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/skintel-ai.git
cd skintel-ai
```

### 2. Install Python Packages
```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg
- **Linux**:
  ```bash
  sudo apt install ffmpeg
  ```
- **Mac** (Homebrew):
  ```bash
  brew install ffmpeg
  ```
- **Windows**:  
  [Download FFmpeg](https://ffmpeg.org/download.html) and add to PATH

### 4. Set API Key
Create `.env` file:
```env
GROQ_API_KEY="your-api-key-here"
```
*Get API key from [Groq Cloud](https://console.groq.com/keys)*

## Usage
```bash
python skintel_main.py
```
The web interface will launch at `http://localhost:7860`

**Workflow:**
1. Upload a skin image (JPEG/PNG)
2. Click the microphone icon to record your question
3. Wait for AI analysis (10-15 seconds)
4. Receive text diagnosis + voice response

## Configuration
| Environment Variable | Description                  |
|----------------------|------------------------------|
| `GROQ_API_KEY`        | Groq Cloud API key (required)|

## Troubleshooting
**Common Issues:**
- **Microphone Not Working**: Check system permissions
- **FFmpeg Errors**: Verify installation with `ffmpeg -version`
- **API Errors**: Ensure valid `GROQ_API_KEY` in environment
- **Audio Playback Issues**: Update sound drivers

## To RUN CODE
Go to Terminal and type " python main_file_name"
Then in Terminal it shows HTTP Request: GET <your url> for webpage .

## License
MIT License - See [LICENSE](LICENSE)

## Contributing
PRs welcome! Please open an issue first to discuss changes.
```

This README:
1. Trying to add RAG/history features per request in future
2. Provides clear setup instructions
3. Documents key functionality
4. Includes troubleshooting tips
5. Maintains platform-agnostic approach

Add a screenshot and customize the repository URLs before use.
