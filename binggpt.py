#gpt bard stop final code...need to be cleaned and add features from gpt_bard_voice_assisstant.py
import speech_recognition as sr
import boto3
import os
import pygame
import openai
from collections import deque
from Bard import Chatbot
import re

# Initialize speech recognition
recognizer = sr.Recognizer()
microphone = sr.Microphone()
recognizer.energy_threshold = 300

# Initialize Amazon Polly client and set default voice
polly_client = boto3.Session(
    aws_access_key_id="YOUR_ACCESS_KEY_ID",
    aws_secret_access_key="YOUR_SECRET_ACCESS_KEY",
    region_name="YOUR_REGION"
).client('polly')

voices = polly_client.describe_voices(LanguageCode='en-US')['Voices']
default_voice = 'Joey'

# OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Bard Token
token = "YOUR_TOKEN"
chatbot = Chatbot(token)

# History for remembering commands
history = deque(maxlen=10)

# Initialize chat history
chat_history = [{'role': 'system', 'content': "You are a helpful assistant."}]

# Global variable to control stopping of speech
stop_speaking = False


def speak(text, voice=default_voice, speed='fast'):
    global stop_speaking
    if stop_speaking:
        stop_speaking = False  # Reset the stop_speaking flag
        return
    response = polly_client.synthesize_speech(
        VoiceId=voice,
        Text=f'<speak><prosody rate="{speed}">{text}</prosody></speak>',
        TextType='ssml',
        OutputFormat='mp3',
        Engine='neural'
    )
    with open('output.mp3', 'wb') as f:
        f.write(response['AudioStream'].read())

    pygame.mixer.init()
    pygame.mixer.music.load('output.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    os.remove('output.mp3')  # Clean up the audio file after playing


def prompt_bard(prompt):
    response = chatbot.ask(prompt)
    return response['content']


# Listen for the wake word and return who was called
def wake_listen():
    print("Waiting for wake word...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        value = recognizer.recognize_google(audio)
        print("You said:{}".format(value))
        if "gpt" in value.lower():
            return "gpt"
        elif "google" in value.lower():
            return "google"
        else:
            return None
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print("Error: {}".format(e))
        return None


def prompt_user(called):
    initial_prompt = True
    while True:
        with microphone as source:
            audio = recognizer.listen(source)
        try:
            value = recognizer.recognize_google(audio)
            if value is None:  # handle case where recognizer.recognize_google returns None
                print("Failed to recognize speech, trying again...")
                continue
            print("You said:{}".format(value))
            if re.search(r"\bok stop\b", value, re.IGNORECASE):
                print("OK, stopping.")
                speak("OK, stopping.")
                break
            elif "gpt" in value.lower() or "google" in value.lower():
                break
            if initial_prompt:
                initial_text = "You are a humanoid robot. You will give all answers as you are interacting like a human with a human. You will give short answers, just one line answers. Change your style and tone according to the user's question. Be sarcastic at times. Remember, you are talking to a friend so don't be so serious always. Act like a human and answer like a human."
                value = initial_text + value
                initial_prompt = False
            if called == "gpt":
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[*chat_history, {'role': 'user', 'content': value}],
                    temperature=0.7,
                )
                print("Response: {}".format(response['choices'][0]['message']['content'].strip()))
                speak(response['choices'][0]['message']['content'].strip(), default_voice)
                chat_history.append(
                    {'role': 'assistant', 'content': response['choices'][0]['message']['content'].strip()})
            else:
                response = prompt_bard(value)
                print("Response: {}".format(response))
                speak(response, default_voice)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Error: {}".format(e))


try:
    while True:
        called = wake_listen()
        if called == "gpt":
            speak("Hello, GPT-3 here! How can I assist you today?")
            chat_history.append({'role': 'assistant', 'content': "Hello, GPT-3 here! How can I assist you today?"})
            prompt_user(called)
        elif called == "google":
            speak("Hello, Bard here! What can I do for you today?")
            prompt_user(called)
        else:
            print("Wake word not recognized. Please say either 'gpt' or 'google'.")

except KeyboardInterrupt:
    pass
