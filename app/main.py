import io
import os
from flask import Flask, render_template, request, jsonify
from google.cloud import vision
from google.cloud import translate_v2 as translate

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image_file' in request.files:
            image_file = request.files['image_file']
            
            # Detect text in the image
            detected_text = detect_text_in_image(image_file)
            
            if detected_text:
                # Translate the detected text
                translated_text = translate_text(detected_text)
                return jsonify({'translated_text': translated_text})
            else:
                return jsonify({'error': 'No text detected in the image.'})
    
    return render_template('index.html')

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
    result = translate_client.translate(text, target_language='en')
    return result['translatedText']

if __name__ == "__main__":
    app.run(debug=True)
