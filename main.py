import azure.cognitiveservices.speech as speechsdk
import openai
import time
import threading

#[Microphone] -> [Azure Continuous Speech Recognition] -> [Silence Detected] -> [Send to OpenAI] -> [Get Response] -> [Bot Replies in speech]

# === CONFIG ===
AZURE_SPEECH_KEY = "Your_Azure_key"
AZURE_REGION = "eastus" #Use eastus while creating service for more speech features
OPENAI_API_KEY = "Your_Open_AI_Key"


# === SETUP ===
speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_REGION)
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
speech_config.speech_synthesis_voice_name = "en-IN-AaravNeural"
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

openai.api_key = OPENAI_API_KEY

# === GLOBALS ===
last_text = ""
last_speech_time = time.time()
silence_timeout = 2.0  # seconds

# === RECOGNITION HANDLER ===
def recognized_handler(evt):
    global last_text, last_speech_time
    if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized: {evt.result.text}")
        last_text += " " + evt.result.text
        last_speech_time = time.time()

# === SILENCE DETECTOR ===
def silence_detector():
    global last_text
    while True:
        time.sleep(0.5)
        if last_text and (time.time() - last_speech_time) > silence_timeout:
            print("\n--- Silence detected, sending to OpenAI ---\n")
            response = call_openai(last_text.strip())
            print("\nBot:", response, "\n")
            speak_response(response)
            last_text = ""  # reset

# === OPENAI CALL ===
def call_openai(prompt_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant talking about Titan Company Products. Keep your response to only 2 sentences"},
            {"role": "user", "content": prompt_text}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

# === TTS ===
def speak_response(text):
    result = speech_synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesis succeeded.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")

# === MAIN ===
speech_recognizer.recognized.connect(recognized_handler)
speech_recognizer.start_continuous_recognition()

# Start silence detector thread
t = threading.Thread(target=silence_detector, daemon=True)
t.start()

print("Bot is listening... Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopping...")
    speech_recognizer.stop_continuous_recognition()
