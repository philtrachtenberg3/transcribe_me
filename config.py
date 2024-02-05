import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    GOOGLE_CLOUD_PROJECT = os.environ.get('GOOGLE_CLOUD_PROJECT') or 'your_project_id'
    
    # Google Cloud Vision API settings
    GOOGLE_CLOUD_VISION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

    # Google Cloud Translate API settings
    GOOGLE_CLOUD_TRANSLATE_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
