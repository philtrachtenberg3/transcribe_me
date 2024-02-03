import io
import os
from flask import Flask, render_template, request, jsonify
from google.cloud import vision
from google.cloud import translate_v2 as translate

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    translated_text = ""
    detected_lang = ""
    if request.method == 'POST':
        if 'image_file' in request.files:
            image_file = request.files['image_file']
            
            # Detect text in the image
            detected_text = detect_text_in_image(image_file)
            
            if detected_text:
                # Translate the detected text and get the detected language code
                detected_lang_code, translated_text = translate_text(detected_text)
                
                # Convert the language code to a language name
                detected_lang = get_language_name(detected_lang_code)
    
    return render_template('index.html', translated_text=translated_text, detected_lang=detected_lang)




def detect_text_in_image(image_file):
    client = vision.ImageAnnotatorClient()

    # Load the image into memory
    content = image_file.read()
    image = vision.Image(content=content)

    # Perform text detection
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description
    return None

def translate_text(text):
    translate_client = translate.Client()

    # Detect the language of the text
    detection = translate_client.detect_language(text)
    lang = detection['language']

    # Translate the text
    result = translate_client.translate(text, target_language='en')

    # Return both the detected language and the translated text
    return lang, result['translatedText']

def get_language_name(lang_code):
    # Map of language codes to language names
    language_codes = {
    'iw': 'Hebrew',
    'en': 'English',
    'es': 'Spanish',
    'ru': 'Russian',
    'ar': 'Arabic',
    'fa': 'Farsi',
    'de': 'German',
    'fr': 'French',
    'it': 'Italian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh-CN': 'Chinese (Simplified)',
    'zh-TW': 'Chinese (Traditional)',
    'pt': 'Portuguese',
    'pt-BR': 'Portuguese (Brazil)',
    'pt-PT': 'Portuguese (Portugal)',
    'hi': 'Hindi',
    'ur': 'Urdu',
    'sw': 'Swahili',
    'nl': 'Dutch',
    'sv': 'Swedish',
    'fi': 'Finnish',
    'no': 'Norwegian',
    'da': 'Danish',
    'pl': 'Polish',
    'tr': 'Turkish',
    'el': 'Greek',
    'he': 'Hebrew',  # Modern code for Hebrew
    # Add more mappings as needed
}

    # Return the language name or the original code if not found
    return language_codes.get(lang_code, lang_code)



if __name__ == "__main__":
    app.run(debug=True)