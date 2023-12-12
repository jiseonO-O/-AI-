import logging
import azure.cognitiveservices.speech as speechsdk
from mtranslate import translate
from konlpy.tag import Kkma
import os
import wave
import pyaudio
import requests
import json
import urllib
from PIL import Image
import nltk
from nltk.corpus import wordnet

nltk.download('wordnet')

REST_API_KEY = 'ed2179da82ee0a21fcdd3e8a303fa209'
subscription_key = "e4a16363c9394dab89cee15b16fc84dd"
region = "koreacentral"

speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
speech_config.speech_recognition_language = "ko-KR"

def custom_word_split(translated_text):
    word_list = []
    current_word = ""
    for char in translated_text:
        if char != ' ':
            current_word += char
        else:
            if current_word:
                word_list.append(current_word)
                current_word = ""
    if current_word:
        word_list.append(current_word)
    return word_list

def SST(text):
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.speech_synthesis_language = "ko-KR"
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    try:
        result = synthesizer.speak_text_async(text).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            audio_data = result.audio_data
        else:
            print(f"음성 변환 실패: {result.reason}")

            cancellation_details = result.cancellation_details
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"::: ErrorCode={cancellation_details.error_code}")
                print(f"::: ErrorDetails=[{cancellation_details.error_details}]")
    except Exception as ex:
        print(f"에러 발생: {ex}")


def SSTen(text):
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.speech_synthesis_language = "en-US"  # 한글 언어 코드
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    try:
        result = synthesizer.speak_text_async(text).get()  # get()을 사용하여 Future를 기다립니다.
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            audio_data = result.audio_data
        else:
            print(f"음성 변환 실패: {result.reason}")

            cancellation_details = result.cancellation_details
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print(f"::: ErrorCode={cancellation_details.error_code}")
                print(f"::: ErrorDetails=[{cancellation_details.error_details}]")
    except Exception as ex:
        print(f"에러 발생: {ex}")


def azure_speech_to_text():
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    print("마이크 ON")
    result = recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return None
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech Recognition canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")
        return None

def find_antonyms(word):
    antonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            if lemma.antonyms():
                antonyms.extend(ant.name() for ant in lemma.antonyms())

    return antonyms

def t2i(translated_text,stte):
    r = requests.post(
        'https://api.kakaobrain.com/v2/inference/karlo/t2i',
        json={
            'prompt': translated_text,
            'negative_prompt': stte
        },
        headers={
            'Authorization': f'KakaoAK {REST_API_KEY}',
            'Content-Type': 'application/json'
        }
    )
    print(translated_text,stte)
    response = json.loads(r.content)
    return response


def main():
    text = azure_speech_to_text()
    #print("Original Text:", text)
    #SST(text)
    if text:
        translated_text = translate(text,"en")
        translated_text = translated_text.replace(".","")
        print("Translated Text:", translated_text)
        words = custom_word_split(translated_text)
        SSTen(translated_text)
        all_antonyms = []
        for word in words:
            antonyms = find_antonyms(word)
            all_antonyms.extend(antonyms)
    else:
        print("Speech recognition failed.")
    if all_antonyms:
        stte = " ".join(all_antonyms)
        print("입력한 문장의 반의어",stte)
    else:
        print("반의어를 찾을 수 없음")
        stte = "icon null Empty space abstract Unrealistic Apathetic Unpleasant " \
                          "Anxious Gloomy Pessimistic Negative"
    response = t2i(translated_text,stte)
    images = response.get("images")
    if images and len(images) > 0:
        result = Image.open(urllib.request.urlopen(images[0].get("image")))
        result.show()
        result.save('image_create.png', 'PNG')
    else:
        print("No valid images found in the response.")
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()