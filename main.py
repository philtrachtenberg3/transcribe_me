from flask import Flask, render_template, request
from google.cloud import translate_v2 as translate

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def translate_text():
    if request.method == 'POST':
        # Get the text to translate from the form
        text = request.form['text']

        # Translate the text using the Google Cloud Translation API
        translated_text = translate_text(text)

        # Render the translated text in the template
        return render_template('index.html', translated_text=translated_text)
    else:
        return render_template('index.html')

def translate_text(text):
    # Initialize the translation client
    translate_client = translate.Client()

    # Translate the text
    result = translate_client.translate(text, target_language='en')

    # Return the translated text
    return result['translatedText']

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
