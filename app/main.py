import os
from flask import Flask, render_template, request
from google.cloud import vision
from google.cloud import translate_v2 as translate  # Consider updating to v3

# Initialize Flask app
app = Flask(__name__)

# Create client instances
vision_client = vision.ImageAnnotatorClient()
translate_client = translate.Client()

@app.route('/', methods=['GET', 'POST'])
def index():
    translated_text = ""
    detected_lang_name = ""
    detected_text = ""
    if request.method == 'POST' and 'image_file' in request.files:
        image_file = request.files['image_file']
        
        detected_text, detected_lang_code = detect_text_in_image(image_file)
        
        if detected_text:
            detected_lang_name, translated_text = translate_text(detected_text, detected_lang_code)

    return render_template('index.html', detected_text=detected_text, translated_text=translated_text, detected_lang=detected_lang_name)

def detect_text_in_image(image_file):
    # Load the image into memory
    content = image_file.read()
    image = vision.Image(content=content)

    # Perform text detection
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        # Assuming the first language in response is the most relevant
        detected_lang_code = response.text_annotations[0].locale if response.text_annotations else 'und'
        return texts[0].description, detected_lang_code
    return None, None

def translate_text(text, lang_code):
    # Note: Update this section to use translate_v3 for better practices
    result = translate_client.translate(text, target_language='en', source_language=lang_code)

    # Assuming the function get_language_name(lang_code) exists and returns the full language name
    return get_language_name(lang_code), result['translatedText']

def get_language_name(lang_code):
    # Implement this function based on your requirements
    # It should return the language name given a language code
    pass

if __name__ == "__main__":
    app.run(debug=True)
