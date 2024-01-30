from flask import Flask, render_template, request, jsonify
from google.cloud import speech, translate_v2 as translate
import os
import subprocess
import uuid
import io

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\philt\Secrets\translation-app-412508-9dd52cf18013.json"

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if an audio file is in the POST request
        if 'audio_file' in request.files:
            audio_file = request.files['audio_file']
            if audio_file.filename.endswith('.mp4'):
                # Process the MP4 file
                audio_path = extract_audio_from_video(audio_file)
                if audio_path:
                    transcribed_text = transcribe_audio(audio_path)
                    translated_text = translate_text(transcribed_text)
                    # Clean up temporary audio file
                    os.remove(audio_path)
                else:
                    return jsonify({'error': 'Audio extraction failed.'})
            else:
                # Process the audio file directly
                audio_blob = audio_file.read()
                transcribed_text = transcribe_audio(audio_blob)
                translated_text = translate_text(transcribed_text)

            return jsonify({'translated_text': translated_text})
    
    return render_template('index.html')

def extract_audio_from_video(video_file):
    unique_filename = str(uuid.uuid4())
    video_path = f'temp_{unique_filename}.mp4'
    audio_path = f'temp_{unique_filename}.mp3'

    video_file.save(video_path)

    # Use ffmpeg to extract audio
    command = ['ffmpeg', '-i', video_path, '-q:a', '0', '-map', 'a', audio_path, '-y']
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Remove the video file after extracting the audio
    os.remove(video_path)

    return audio_path if os.path.exists(audio_path) else None

def transcribe_audio(audio_content):
    # Assumes `audio_content` is the path to the audio file
    with io.open(audio_content, 'rb') as audio_file:
        content = audio_file.read()

    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=44100,
        language_code='en-US',
    )

    response = client.recognize(config=config, audio=audio)
    transcription = ' '.join(result.alternatives[0].transcript for result in response.results) if response.results else ''
    return transcription

def translate_text(text):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language='en')
    return result['translatedText']

if __name__ == "__main__":
    app.run(debug=True)
