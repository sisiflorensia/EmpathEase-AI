import os
import random
import re
from flask import Flask, render_template, request, jsonify
import whisper
from transformers import pipeline
import google.generativeai as palm
from gtts import gTTS

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

app = Flask(__name__)

palm.configure(api_key="AIzaSyDvlftPu0O4ZxbbG7DQFc0MeaG3VxQPeLc")
    
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_audio():
    audio_file = request.files.get('audio')
        
    if audio_file:
        filepath = os.path.join("uploads", "received_audio.wav")
        audio_file.save(filepath)
        model = whisper.load_model("base")
        result = model.transcribe(filepath)
        sentiment = speech_to_sentiment(result["text"])
        sentiment_level = int(sentiment[0]["label"][0])
        sentiment_score = sentiment[0]["score"]

        response = apiPalm(result["text"], sentiment_level, sentiment_score)
        cleaned_response = re.sub(r'[^a-zA-Z0-9\s]', '', response)
        audio_path = generate_audio(cleaned_response)

        os.system(f"start {audio_path}")

        combined_result = {
            "transcription": result["text"],
            "sentiment": sentiment,
            "response": response,
            "audio_path": audio_path
        }

        return jsonify(combined_result)
        # return result
    return jsonify({"message": "Failed to upload audio"}), 400

# Initialize the emotion analysis pipeline
emotion_classifier = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
def speech_to_sentiment(transcribed_text):

    # Analyze sentiment in the transcribed text
    sentiment_result = emotion_classifier(transcribed_text)
    return sentiment_result

def apiPalm(message, sentiment_level, sentiment_score):
    # Send the message to Palm's API and receive the response

    empathetic_prompt  = f"Create a concise and great response to this emotional venting message from a user, and promote active listening, by probing with empathetic question and make the them feel heard. Use a maximum 10-word sentence: ${message}"

    calmer_response = [
        "Thank you for sharing. Take care.", 
        "I appreciate your trust. Rest up.",
        "Glad you spoke up. Wishing you well.",
        "Always here to listen. Hope things improve.",
        "Your feelings are valid. Take it easy.",
        "Thank you for confiding. Better days ahead.",
        "I'm here when needed. Look after yourself.",
        "Acknowledging your words. Hope for relief soon.",
        "Grateful you reached out. Stay strong.",
        "Heard and understood. Take your time.",
        "I'm glad you took the time to share your feelings with me. Remember to take care of yourself and reach out whenever you need to talk. Wishing you peace and clarity.",
        "It sounds like you've been through a lot. Remember, it's okay to take a step back and rest when needed. I'm here whenever you want to chat.",
        "Thank you for trusting me with your thoughts. I hope things get better for you soon. Remember, every day is a new opportunity for growth and healing.",
        "I'm always here to lend an ear. Take some time for yourself and know that you're not alone in this. Wishing you strength.",
        "It's important to let out your feelings, and I'm glad you chose to share them with me. Remember to breathe and give yourself the grace to heal. Reach out anytime.",
        "I appreciate you opening up. Life has its challenges, but I believe in your resilience. Take all the time you need, and know I'm here to support you.",
        "Thank you for sharing. It's a sign of strength to seek support when needed. I hope you find the peace and resolution you're looking for. Always here for you.",
        "It's been a journey, hasn't it? Remember to be kind to yourself and know that brighter days are ahead. I'm here whenever you need a listening ear.",
        "Your feelings are valid, and I'm grateful you shared them with me. Wishing you moments of calm and clarity ahead. Don't hesitate to reach out.",
        "It's always a privilege to be here for you. I hope you find the comfort and solutions you seek. Remember, life has its ups and downs, but you're never alone in navigating them."
    ]

    if sentiment_level == 1:
        response = palm.generate_text(prompt=empathetic_prompt)
        return response.result
    elif sentiment_level == 2 and sentiment_score > 0.6:
        response = palm.generate_text(prompt=empathetic_prompt)
        return response.result
    elif sentiment_level == 3 and sentiment_score < 0.4:
        response = palm.generate_text(prompt=empathetic_prompt)
        return response.result
    else: 
        return random.choice(calmer_response)

import datetime
def generate_audio(command):
    tts = gTTS(text=command, lang='en')
    now = datetime.datetime.utcnow()
    audio_path = "./static/" + str(now) + ".mp3"
    tts.save(audio_path)
    return audio_path

if __name__ == '__main__':
    app.run(host='localhost', port = 5000, debug=True)
