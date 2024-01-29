from flask import Flask, render_template, request
from google.cloud import translate_v2 as translate

app = Flask(__name__)

# Renamed the view function to avoid conflict with the translation function
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the text to translate from the form
        text = request.form['text']

        # Translate the text using the separate translation function
        translated_text = translate_text(text)

        # Render the translated text in the template
        return render_template('index.html', translated_text=translated_text)
    else:
        # No text to translate, just render the template
        return render_template('index.html')

# Utility function to perform translation, distinct from the view function
def translate_text(text):
    # Initialize the translation client
    translate_client = translate.Client()

    # Translate the text
    result = translate_client.translate(text, target_language='en')

    # Return the translated text
    return result['translatedText']

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
