import os
import sys

import requests
import json
from playsound import playsound
from google.cloud import speech, texttospeech

import RealTimeAudio
# import Mic

RATE = 16000
CHUNK = int(RATE / 10)

# Change this according to your google crediential API key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'robust-arcadia-339212-6b023c978fb5.json'

webhook_url = "http://localhost:5005/webhooks/rest/webhook"
username = "ibt"


def sendMessage(message):
    if message == "exit":
        sys.exit(0)

    data = {
        "sender": username,
        "message": message
    }

    response = requests.post(webhook_url, data=json.dumps(
        data), headers={"Content-Type": "application/json; charset=UTF-8"})

    strippedResponse = response.text.strip("[]")
    responses = []
    if "},{" in strippedResponse:
        while True:
            location = strippedResponse.find("},{")
            if location == -1:
                responses.append(strippedResponse)
                break
            responses.append(strippedResponse[:location+1])
            strippedResponse = strippedResponse[location+2:]
    else:
        responses.append(strippedResponse)
    for response in responses:
        jsonResponse = json.loads(response)
        if jsonResponse.get("text", False):
            responseText = jsonResponse["text"]
            print("Rasa: ", responseText)
            textToSpeech(responseText)
        if jsonResponse.get("image", False):
            print("Rasa: ", jsonResponse["image"])


def speechToText():
    language_code = "tr-TR"  # Change this according to your language
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )
    with RealTimeAudio.MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )
        responses = client.streaming_recognize(streaming_config, requests)
        theText = RealTimeAudio.listen_print_loop(responses)
        sendMessage(theText)


"""
# Non real time speech to text function
def speechToText():
    client = speech.SpeechClient()
    audioFile = io.open("demo.wav", "rb")
    content = audioFile.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        # encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        sample_rate_hertz=44100,
        language_code="tr-TR",
        # audio_channel_count=2,
        enable_word_time_offsets=True
    )
    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        theText = result.alternatives[0].transcript
        print(theText)
        sendMessage(theText)
"""


def textToSpeech(message):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=message)
    voice = texttospeech.VoiceSelectionParams(
        language_code="tr-TR", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)  # Change this according to your language
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
    playsound('output.mp3')


while True:
    speechToText()
