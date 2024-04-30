from pytube import YouTube

url = "https://www.youtube.com/watch?v=BCWAXW7tLZg"

try:
   video = YouTube(url)
   #stream = video.streams.filter(only_audio=True).first()
   #stream = video.streams.filter(only_audio=True).get_by_itag(251)
   stream = video.streams.filter(only_audio=True).get_by_itag(140)
   #stream = video.streams.filter(only_audio=True)
   #print(stream)
   stream.download(filename=f"Jeans_Song_1.wav")
   print("The video is downloaded in MP3")
except KeyError:
   print("Unable to fetch video information. Please check the video URL or your network connection.")