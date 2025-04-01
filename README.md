# AISpeechBot

# 🎙️ Azure + OpenAI Speech Bot

This project is a simple speech bot pipeline integrating Azure Cognitive Services (Speech SDK) and OpenAI GPT-3.5 Turbo. It listens through your microphone, detects silence, sends the transcript to OpenAI, and reads out the response using Azure's Text-to-Speech.

---

## 🛠 Features

- Continuous speech recognition using Azure Speech SDK.
- Detects silence to trigger sending text to OpenAI.
- OpenAI GPT-3.5 Turbo generates a short reply.
- Azure Text-to-Speech (TTS) reads out the reply.
- Designed for Titan Company product-related conversations (customizable).

---

## 📦 Requirements

- Python 3.8+
- Azure Cognitive Services Speech SDK
- OpenAI Python SDK

---

## ⚙️ Installation

```bash
git clone https://github.com/yourusername/speech-bot.git
cd speech-bot
pip install -r requirements.txt
