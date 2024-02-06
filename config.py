import os

class Config:
    # Environment variables are used to configure the application.
    # The 'or' fallbacks can be defaults or None if you want to enforce the setting via environment variables.
    
    # Secret Key for Flask application, necessary for session management, CSRF protection, etc.
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Google Cloud Project ID
    GOOGLE_CLOUD_PROJECT = os.environ.get('GOOGLE_CLOUD_PROJECT')

    # Any other configuration variables can be added here as needed, for example:
    # DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///default.db'
