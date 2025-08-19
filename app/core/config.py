import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('env.production')

class Settings:
    """Application settings"""
    
    # Google Drive API settings
    GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
    GOOGLE_TOKEN_FILE = os.getenv("GOOGLE_TOKEN_FILE", "token.json")
    
    # API settings
    API_TITLE = "Google Drive API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "Google Drive integration API"
    
    # CORS settings
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://*.netlify.app",  # Netlify sites
        "https://*.onrender.com",  # Render.com API
    ]

settings = Settings() 