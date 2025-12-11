from gtts import gTTS
import os

# The text you want to convert
my_text = 'Happy Birthday Irshita'

# Generate the audio
language = 'en'
my_obj = gTTS(text=my_text, lang=language, slow=False)

# Save the file
filename = "happy_birthday_irshita.mp3"
my_obj.save(filename)

print(f"Audio saved as {filename}")