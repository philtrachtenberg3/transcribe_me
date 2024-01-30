from flask import Flask, render_template, request
from google.cloud import speech, translate_v2 as translate
import os

app = Flask(__name__)

# Configure this environment variable in your operating system
# or define it before running the Flask app
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\philt\Secrets\client_secret_408217728727-cojkas93hrrh997j06ng6sgim6a6jmrl.apps.googleusercontent.com (1).json"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if an audio file is in the POST request
        if 'audio_file' in request.files:
            audio_file = request.files['audio_file']
            # Here you would usually save the file and then process it
            # For simplicity, let's assume we're sending it directly to the Speech-to-Text API
            
            # Transcribe audio file
            transcribed_text = transcribe_audio(audio_file)
            
            # Translate text
            translated_text = translate_text(transcribed_text)
            
            return render_template('index.html', translated_text=translated_text)
    else:
        return render_template('index.html')

def transcribe_audio(audio_file):
    # Initialize the Google Cloud Speech client
    client = speech.SpeechClient()

    # TODO: Process the audio file as needed for Google Speech-to-Text
    # For example, you might need to convert it to the proper format (e.g., FLAC)

    # Now, let's assume the audio file is in the proper format
    audio_content = audio_file.read()
    audio = speech.RecognitionAudio(content=audio_content)
    
    config = speech.RecognitionConfig(
        # You will need to determine the appropriate encoding and sample rate for your audio file
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code="en-US",  # Change to the appropriate language of the audio
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)
    
    # Just for simplicity, returning the first result here
    return response.results[0].alternatives[0].transcript if response.results else ''

def translate_text(text):
    # Initialize the translation client
    translate_client = translate.Client()

    # Translate the text
    result = translate_client.translate(text, target_language='en')
    
    # Return the translated text
    return result['translatedText']

if __name__ == "__main__":
    app.run(debug=True)
