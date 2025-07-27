# 🎬 YouTube Video Transcriber

This Python project allows you to transcribe YouTube videos using **OpenAI's Whisper** or **YouTube's own subtitles** (when available).

- ✅ Works on **Windows**, **macOS**, and **Linux**
- 🧠 Supports **Whisper AI** for local/offline transcription
- ⚡ Automatically fetches **YouTube captions** when available (faster)

## 🚀 How to Use

1. **Clone the repository:**
```bash
git clone https://github.com/dflucas/youtube-video-transcriber
cd youtube-video-transcriber
```

## Install dependencies:

```bash
pip install yt-dlp openai-whisper youtube-transcript-api
```
💡 You also need ffmpeg for Whisper to work properly.

On Windows, download it from ffmpeg.org.

On macOS, use Homebrew: ```brew install ffmpeg```

On Linux (Debian/Ubuntu), use apt: ```sudo apt install ffmpeg```

## Run the script:

```bash
python youtube_to_text.py
```
You'll be prompted to enter a YouTube video URL. The script will:
- Try to download subtitles via the YouTube Transcript API.
- If unavailable, it will download the video’s audio and transcribe it with Whisper.
- Save the transcript as a ```.txt``` file in the project folder.

## 📄 Example Output
```bash
Transcript for: "How to Learn Python in 10 Minutes"

Welcome to this crash course on Python...
...
```
## 📚 Requirements

Python 3.8+

```yt-dlp```

```openai-whisper```

```youtube-transcript-api```

```ffmpeg``` (only required if Whisper is used)

## 🧠 About Whisper

Whisper is a general-purpose speech recognition model by OpenAI trained on a large dataset of multilingual and multitask supervised data collected from the web.

More info: https://github.com/openai/whisper

## License
MIT License. See [LICENSE](https://choosealicense.com/licenses/mit/) for more information.

