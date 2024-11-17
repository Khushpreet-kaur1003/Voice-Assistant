import speech_recognition as aa
import pywhatkit
import datetime
import wikipedia
import streamlit as st
from gtts import gTTS
import io
import pygame
import threading

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Initialize speech recognizer
listener = aa.Recognizer()

# Function to speak text using gTTS without opening media player, with increased speed
def talk(text):
    tts = gTTS(text=text, lang='en', slow=False)  # Increased speed by setting slow=False
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    
    # Load the audio into pygame and play it
    pygame.mixer.music.load(audio_fp, 'mp3')
    pygame.mixer.music.play()

    # Keep the script running until the audio finishes playing
    while pygame.mixer.music.get_busy():
        continue

# Function to capture voice input with timeout
def input_instruction():
    try:
        with aa.Microphone(device_index=None) as origin:
            st.write("Listening...")
            listener.adjust_for_ambient_noise(origin, duration=0.2)
            speech = listener.listen(origin, timeout=5)  # Set timeout
            instruction = listener.recognize_google(speech)
            instruction = instruction.lower()
            st.write(f"Recognized instruction: {instruction}")
            return instruction
    except aa.UnknownValueError:
        talk("Sorry, I couldn't understand the audio.")
        st.write("Google Speech Recognition could not understand the audio")
    except aa.RequestError as e:
        talk("Sorry, I'm having trouble connecting to the speech recognition service.")
        st.write(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        talk("An error occurred.")
        st.write(f"An unexpected error occurred: {e}")
        return None

# Function to handle YouTube playback in a separate thread
def play_song(song):
    pywhatkit.playonyt(song)

# Function to execute JARVIS commands
def play_Jarvis(instruction):
    if instruction is None:
        st.write("No valid instruction captured.")
        return

    if 'play' in instruction:
        song = instruction.replace('play', '')
        talk(f"Playing {song}")
        st.write(f"Playing {song}")
        # Use threading to prevent blocking
        threading.Thread(target=play_song, args=(song,)).start()

    elif 'time' in instruction:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f'Current time is {time}')
        st.write(f'Current time is {time}')

    elif 'date' in instruction:
        date = datetime.datetime.now().strftime('%d/%m/%Y')
        talk(f"Today's date is {date}")
        st.write(f"Today's date is {date}")

    elif 'how are you' in instruction:
        talk("I am fine, how about you?")
        st.write("I am fine, how about you?")

    elif 'what is your name' in instruction:
        talk("I am Jarvis, how can I help you?")
        st.write("I am Jarvis, how can I help you?")

    elif any(keyword in instruction for keyword in ['who', 'which', 'what', 'how', 'when', 'give', 'name']):
        query = instruction.replace('who','').replace('which','').replace('what','').replace('how','').replace('when','').replace('give','').replace('name few','').strip()
        st.write(f"Searching Wikipedia for: {instruction}")
        try:
            info = wikipedia.summary(query, sentences=3)
            st.write(info)
            talk(info)
        except wikipedia.exceptions.DisambiguationError:
            talk("There are multiple results, please be more specific.")
            st.write("There are multiple results, please be more specific.")
        except wikipedia.exceptions.PageError:
            talk("Sorry, I couldn't find any information on that.")
            st.write("Sorry, I couldn't find any information on that.")

    else:
        talk("Please repeat the instruction.")
        st.write("Please repeat the instruction.")

# Streamlit GUI
st.title("JARVIS Virtual Assistant")

# Combine Speak and Submit buttons in a single row
col1, col2 = st.columns(2)

with col1:
    instruction_text = st.text_input("Enter your command:")

with col2:
    if st.button("Speak"):
        instruction_voice = input_instruction()
        play_Jarvis(instruction_voice)

    if st.button("Submit"):
        play_Jarvis(instruction_text)
