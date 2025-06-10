import os
from dotenv import load_dotenv

# Determine the current environment (dev, qa, prod)
# Default to 'dev' if APP_ENV is not set
env = os.getenv("APP_ENV", "dev").lower()

# Construct the path to the environment-specific .env file
dotenv_path = f".env.{env}"

# Load the environment variables from the specified file
# The load_dotenv function will gracefully handle if the file doesn't exist.
load_dotenv(dotenv_path=dotenv_path)

print(f"Loading settings from {dotenv_path}")

# --- Database Configuration ---
# Load database settings from environment variables with sensible defaults.
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "default_db_name")
DB_USER = os.getenv("DB_USER", "default_db_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "default_db_password")
DB_PORT = os.getenv("DB_PORT", "5432")

# --- API Configuration ---
# Load API settings.
API_ENDPOINT = os.getenv("API_ENDPOINT", "https://api.example.com/upload")
API_KEY = os.getenv("API_KEY", "your_api_key_if_needed")

# --- File Configuration ---
# Load file output settings.
OUTPUT_FILE_DIRECTORY = os.getenv("OUTPUT_FILE_DIRECTORY", "output_files")
OUTPUT_FILE_NAME = os.getenv("OUTPUT_FILE_NAME", "data_export.csv")

# --- Application-wide settings ---
# You can also have a general setting for the environment name
APP_ENVIRONMENT = env

# Ensure the output directory exists
os.makedirs(OUTPUT_FILE_DIRECTORY, exist_ok=True)