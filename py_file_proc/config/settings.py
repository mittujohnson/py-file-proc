# your_project_name/config/settings.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "your_database_name")
DB_USER = os.getenv("DB_USER", "your_db_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_db_password")
DB_PORT = os.getenv("DB_PORT", "5432")

# API Configuration
API_ENDPOINT = os.getenv("API_ENDPOINT", "https://api.example.com/upload")
API_KEY = os.getenv("API_KEY", "your_api_key_if_needed")

# File Configuration
OUTPUT_FILE_DIRECTORY = os.getenv("OUTPUT_FILE_DIRECTORY", "output_files")
OUTPUT_FILE_NAME = os.getenv("OUTPUT_FILE_NAME", "data_export.csv")

# Ensure the output directory exists
os.makedirs(OUTPUT_FILE_DIRECTORY, exist_ok=True)