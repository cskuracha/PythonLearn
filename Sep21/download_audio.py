from pytube import Playlist, YouTube
from moviepy.editor import AudioFileClip
import os

# Function to download audio from a YouTube video
def download_audio(url, output_path='downloads'):
    try:
        yt = YouTube(url)
        print(f"Downloading: {yt.title}")

        # Get the highest quality audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()
        downloaded_file = audio_stream.download(output_path=output_path)

        # Convert to mp3
        mp3_file = os.path.splitext(downloaded_file)[0] + ".mp3"
        audio_clip = AudioFileClip(downloaded_file)
        audio_clip.write_audiofile(mp3_file)
        audio_clip.close()

        # Remove original file (optional)
        os.remove(downloaded_file)

        print(f"Saved as MP3: {mp3_file}\n")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

# Function to download all songs from a playlist
def download_playlist(playlist_url, output_path='downloads'):
    pl = Playlist(playlist_url)
    print(f"Found {len(pl.video_urls)} videos in playlist.\n")

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for video_url in pl.video_urls:
        download_audio(video_url, output_path)

# Example usage
playlist_url = input("Enter YouTube playlist URL: ")
download_playlist(playlist_url)
