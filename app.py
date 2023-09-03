# import io
import os
from flask import Flask, render_template, render_template_string, request, jsonify
import openai
from scipy.io import wavfile
import openai
import whisper
# import numpy as np
# from tempfile import NamedTemporaryFile

# # Get the uploaded file from request
# audio_file = request.files.get('file')

# # Save it to a temporary location
# temp_file = NamedTemporaryFile(delete=False, suffix=".wav")
# audio_file.save(temp_file.name)

# # Now load it using whisper
# audio = whisper.load_audio(temp_file.name)

# Once done, you can delete the temporary file
#os.unlink(temp_file.name)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')


app = Flask(__name__)

openai.api_key = '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'
    
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])


def upload_audio():
    audio_file = request.files.get('audio')
        
    if audio_file:
        filepath = os.path.join("uploads", "received_audio.wav")
        audio_file.save(filepath)
        # You can process the audio file here...
        model = whisper.load_model("base")
        result = model.transcribe(filepath)
        # text_result = result["text"]
        return result
    return jsonify({"message": "Failed to upload audio"}), 400

# def get_sentiment(text):
#     response = openai.Completion.create(
#         engine="text-davinci-002",
#         prompt=f"Sentiment analysis of the following text:\n{text}\n",
#         temperature=0.5,
#         max_tokens=1,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0,
#         stop=["\n"]
#     )

#     sentiment = response.choices[0].text.strip()
#     return sentiment
    
# @app.route('/process_audio', methods=['POST'])
# def process_audio():
#     model = whisper.load_model("base")
        
#     # audio_file = request.files.get("file")
#             # wav_data = audio_file.read()

#         # sample_rate, audio_data = wavfile.read(io.BytesIO(wav_data))
#         # numpy_array = np.array(audio_data)

#         # result = model.transcribe(numpy_array)


#     # with open("transcription.txt", "w", encoding="utf-8") as txt:
#     #     txt.write(result["text"])

#     # Get the uploaded file from request
#     audio_file = request.files.get('file')

#     # Save it to a temporary location
#     temp_file = NamedTemporaryFile(delete=False, suffix=".wav")
#     audio_file.save(temp_file.name)

#     # Now load it using whisper
#     audio = whisper.load_audio(temp_file.name)

#     # Once done, you can delete the temporary file
#     os.unlink(temp_file.name)

#     # load audio and pad/trim it to fit 30 seconds
    
#     # make log-Mel spectrogram and move to the same device as the model
#     mel = whisper.log_mel_spectrogram(audio).to(model.device)

#     # detect the spoken language
#     _, probs = model.detect_language(mel)
#     print(f"Detected language: {max(probs, key=probs.get)}")

#     # decode the audio
#     options = whisper.DecodingOptions()
#     result = whisper.decode(model, mel, options)

#     # print the recognized text
#     print(result.text)

if __name__ == '__main__':
    app.run(host='localhost', port = 5000, debug=True)
