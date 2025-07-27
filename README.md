# 🎬 YouTube Video Transcriber

This Python project allows you to transcribe YouTube videos using **OpenAI's Whisper** or **YouTube's own subtitles** (when available).

✅ Works on **Windows**, **macOS**, and **Linux**  
🧠 Supports **Whisper AI** for local/offline transcription  
⚡ Automatically fetches **YouTube captions** when available (faster)

---

## 🔧 Features

- 🔍 Auto-detects and uses YouTube subtitles if available (manual or auto-generated)
- 🧠 Falls back to Whisper AI transcription if no subtitles are found
- ⚙️ Detects missing dependencies and provides usage instructions
- 📁 Saves transcripts to `.txt` files named after the video title
- 🖥️ Outputs transcript preview to terminal

---

## 🚀 How to Use

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/youtube-video-transcriber.git
cd youtube-video-transcriber
pip install yt-dlp openai-whisper youtube-transcript-api
    Install dependencies:

pip install yt-dlp openai-whisper youtube-transcript-api

    💡 You also need ffmpeg for Whisper to work properly.

        On Windows, download it from: https://ffmpeg.org/download.html

        On macOS: brew install ffmpeg

        On Linux (Debian/Ubuntu): sudo apt install ffmpeg

    Run the script:

python transcribe.py

You’ll be prompted to enter a YouTube video URL. The script will:

    Try to download subtitles via the YouTube Transcript API

    If unavailable, download the video’s audio and transcribe it with Whisper

    Save the transcript as a .txt file in the project folder

📄 Example Output

Transcript for: "How to Learn Python in 10 Minutes"

Welcome to this crash course on Python...
...

📚 Requirements

    Python 3.8+

    yt-dlp

    openai-whisper

    youtube-transcript-api

    ffmpeg (only required if Whisper is used)

🧠 About Whisper

Whisper is a general-purpose speech recognition model by OpenAI trained on a large dataset of multilingual and multitask supervised data collected from the web.

More info: https://github.com/openai/whisper
📜 License

MIT License. See LICENSE for more information.


---
