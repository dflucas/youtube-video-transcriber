import pytubefix
import ffmpeg
from openai import OpenAI
import sys

# Get the video URL from the command-line arguments
url = sys.argv[1]
filename = "audio.wav"

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=<OPENAI_API_KEY>) 

# Download the YouTube video using pytubefix
yt = pytubefix.YouTube(url)

# Select the best available audio-only stream
audio_stream = yt.streams.filter(only_audio=True).first()

# Download the audio stream to a temporary file
audio_stream.download(filename="temp_audio.mp4")

# Convert the downloaded audio to WAV format using ffmpeg
ffmpeg.input("temp_audio.mp4").output(
    filename,
    format='wav',
    loglevel="error"
).run(cmd=r"C:\ffmpeg\bin\ffmpeg.exe")  # Make sure ffmpeg is installed and path is correct

# Open the WAV file and send it to Whisper for transcription
with open(filename, "rb") as audio_file:
    transcript_response = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

# Extract the transcribed text
transcript = transcript_response.text

# Generate a summary using GPT-4o-mini
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system",
         "content": "You are an assistant that summarizes videos. Use markdown formatting."},
        {"role": "user",
         "content": f"Summarize the following video transcript:\n\n{transcript}"}
    ]
)

# Save the summary to a markdown file
with open("resumo.md", "w") as md:
    md.write(completion.choices[0].message.content)
