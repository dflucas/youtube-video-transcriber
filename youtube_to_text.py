#!/usr/bin/env python3
"""
YouTube Video Transcriber
A cross-platform tool to transcribe YouTube videos using Whisper AI or YouTube captions.
Supports Windows, macOS, and Linux.
"""

import os
import sys
import re
import subprocess
import platform
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = {
        'yt-dlp': 'yt_dlp',
        'openai-whisper': 'whisper',
        'youtube-transcript-api': 'youtube_transcript_api'
    }
    
    missing_packages = []
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   pip install {package}")
        print("\nInstall missing packages and try again.")
        return False
    
    return True

def setup_ffmpeg_path():
    """Add common FFmpeg paths to system PATH"""
    system = platform.system().lower()
    
    possible_paths = []
    
    if system == "windows":
        possible_paths = [
            "C:\\ffmpeg\\bin",
            "C:\\Program Files\\ffmpeg\\bin",
            str(Path.home() / "ffmpeg" / "bin")
        ]
    elif system == "darwin":  # macOS
        possible_paths = [
            "/usr/local/bin",
            "/opt/homebrew/bin",
            "/usr/bin"
        ]
    else:  # Linux
        possible_paths = [
            "/usr/bin",
            "/usr/local/bin",
            str(Path.home() / ".local" / "bin")
        ]
    
    # Add existing paths to system PATH
    current_path = os.environ.get('PATH', '')
    for path in possible_paths:
        if os.path.exists(path) and path not in current_path:
            os.environ['PATH'] = f"{path}{os.pathsep}{current_path}"

def extract_video_id(url):
    """Extract YouTube video ID from various URL formats"""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def transcribe_with_captions(url):
    """Fast transcription using YouTube's built-in captions"""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        
        video_id = extract_video_id(url)
        if not video_id:
            return None, "Invalid YouTube URL"
        
        print(f"📹 Video ID: {video_id}")
        print("🔍 Searching for captions...")
        
        # Try different languages
        languages = ['en', 'pt', 'es', 'fr', 'de']
        
        for lang in languages:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
                print(f"✅ Captions found in: {lang}")
                
                # Combine all text
                full_text = " ".join([item['text'] for item in transcript])
                return full_text, None
                
            except Exception:
                continue
        
        # Try automatic captions if manual ones fail
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            for transcript in transcript_list:
                if transcript.language_code in languages:
                    data = transcript.fetch()
                    full_text = " ".join([item['text'] for item in data])
                    print(f"✅ Auto-captions found in: {transcript.language_code}")
                    return full_text, None
        except Exception as e:
            return None, f"No captions available: {str(e)}"
    
    except ImportError:
        return None, "youtube-transcript-api not installed"
    
    return None, "No captions found"

def transcribe_with_whisper(url, model_size="tiny"):
    """Transcribe using Whisper AI (slower but works without captions)"""
    try:
        import yt_dlp
        import whisper
        
        # Setup FFmpeg path
        setup_ffmpeg_path()
        
        print("⬇️ Downloading audio...")
        
        # Download configuration
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'outtmpl': 'temp_audio.%(ext)s',
            'quiet': True,
            'no_warnings': True
        }
        
        # Download audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown')
                ydl.download([url])
            except Exception as e:
                return None, f"Download failed: {str(e)}"
        
        # Find downloaded file
        audio_file = None
        for file in os.listdir('.'):
            if file.startswith('temp_audio.'):
                audio_file = file
                break
        
        if not audio_file:
            return None, "Audio file not found after download"
        
        print(f"🎵 Audio downloaded: {audio_file}")
        print(f"🤖 Loading Whisper model: {model_size}")
        
        # Load Whisper model
        model = whisper.load_model(model_size)
        
        print("🔄 Transcribing... (this may take a while)")
        
        # Transcribe
        result = model.transcribe(
            audio_file,
            fp16=False,
            verbose=False
        )
        
        # Cleanup
        try:
            os.remove(audio_file)
            print("🗑️ Temporary audio file removed")
        except:
            print(f"⚠️ Please manually remove: {audio_file}")
        
        return result['text'], None
        
    except ImportError as e:
        return None, f"Missing dependency: {str(e)}"
    except Exception as e:
        return None, f"Whisper transcription failed: {str(e)}"

def clean_filename(filename):
    """Clean filename for cross-platform compatibility"""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove extra spaces and dots
    filename = re.sub(r'[\s.]{2,}', '_', filename)
    # Limit length
    if len(filename) > 200:
        filename = filename[:200]
    return filename.strip()

def save_transcription(text, video_info, method):
    """Save transcription to file"""
    try:
        # Create filename
        title = video_info.get('title', 'youtube_video')
        clean_title = clean_filename(title)
        filename = f"{clean_title}_transcription.txt"
        
        # Save to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"YouTube Video Transcription\n")
            f.write(f"=" * 50 + "\n")
            f.write(f"Title: {title}\n")
            f.write(f"URL: {video_info.get('url', 'N/A')}\n")
            f.write(f"Method: {method}\n")
            f.write(f"Characters: {len(text)}\n")
            f.write("=" * 50 + "\n\n")
            f.write(text)
        
        return filename
    except Exception as e:
        print(f"❌ Failed to save file: {e}")
        return None

def main():
    """Main function"""
    print("🎬 YouTube Video Transcriber")
    print("=" * 40)
    print("Cross-platform transcription tool")
    print("Supports: Windows, macOS, Linux\n")
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Get URL from user
    url = input("📝 Enter YouTube URL: ").strip()
    
    if not url or not any(domain in url for domain in ['youtube.com', 'youtu.be']):
        print("❌ Invalid YouTube URL")
        return
    
    # Get video info
    try:
        import yt_dlp
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            video_info = {
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'url': url
            }
        
        duration_min = video_info['duration'] // 60
        print(f"🎥 Title: {video_info['title']}")
        print(f"⏱️ Duration: {duration_min} minutes")
        
    except Exception:
        video_info = {'title': 'Unknown', 'url': url}
    
    # Choose transcription method
    print("\n🔧 Choose transcription method:")
    print("1. YouTube Captions (Fast, requires captions)")
    print("2. Whisper AI - Tiny (Fast, lower accuracy)")
    print("3. Whisper AI - Base (Slower, better accuracy)")
    
    choice = input("Enter choice (1-3) [default: 1]: ").strip() or "1"
    
    transcription = None
    error = None
    method = ""
    
    if choice == "1":
        method = "YouTube Captions"
        print(f"\n🚀 Using {method}...")
        transcription, error = transcribe_with_captions(url)
    
    elif choice in ["2", "3"]:
        model_size = "tiny" if choice == "2" else "base"
        method = f"Whisper AI ({model_size})"
        print(f"\n🚀 Using {method}...")
        transcription, error = transcribe_with_whisper(url, model_size)
    
    else:
        print("❌ Invalid choice")
        return
    
    # Handle results
    if error:
        print(f"❌ Error: {error}")
        
        # Fallback to other method
        if choice == "1":
            print("\n🔄 Falling back to Whisper AI (tiny)...")
            transcription, error = transcribe_with_whisper(url, "tiny")
            method = "Whisper AI (tiny) - Fallback"
    
    if not transcription:
        print("❌ Transcription failed with all methods")
        return
    
    # Save transcription
    filename = save_transcription(transcription, video_info, method)
    
    if filename:
        print(f"\n✅ Success! Transcription saved to: {filename}")
        print(f"📊 Total characters: {len(transcription)}")
        
        # Show preview
        preview_length = min(300, len(transcription))
        print(f"\n📖 Preview (first {preview_length} characters):")
        print("-" * 50)
        print(transcription[:preview_length] + ("..." if len(transcription) > preview_length else ""))
    else:
        print("\n📄 Raw transcription:")
        print("-" * 50)
        print(transcription)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Transcription cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    
    input("\nPress Enter to exit...")