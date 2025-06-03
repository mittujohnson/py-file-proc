# your_project_name/api_client/api_sender.py

import requests
import os # Import os for path.basename
from your_project_name.config import settings

def upload_file_to_api(filepath: str, api_endpoint: str = settings.API_ENDPOINT, api_key: str = settings.API_KEY) -> bool:
    """
    Uploads a file to a specified API endpoint.

    Args:
        filepath (str): The full path to the file to upload.
        api_endpoint (str): The URL of the API endpoint.
        api_key (str): The API key for authentication (if required by the API).

    Returns:
        bool: True if the upload was successful, False otherwise.
    """
    if not filepath or not os.path.exists(filepath):
        print(f"File not found or invalid path: {filepath}")
        return False

    headers = {}
    if api_key:
        # Example: Add API key to headers. Adjust based on your API's authentication method.
        # Common methods: 'Authorization': 'Bearer YOUR_API_KEY', 'x-api-key': 'YOUR_API_KEY'
        headers['X-API-Key'] = api_key # Or 'Authorization': f'Bearer {api_key}'

    try:
        with open(filepath, 'rb') as f:
            # Determine content type based on file extension
            file_extension = os.path.splitext(filepath)[1].lower()
            if file_extension == '.csv':
                content_type = 'text/csv'
            elif file_extension == '.json':
                content_type = 'application/json'
            elif file_extension == '.xml':
                content_type = 'application/xml' # New content type for XML
            else:
                content_type = 'application/octet-stream' # Default for unknown types

            files = {'file': (os.path.basename(filepath), f, content_type)}
            response = requests.post(api_endpoint, headers=headers, files=files)

            if response.status_code == 200:
                print(f"File '{os.path.basename(filepath)}' uploaded successfully to {api_endpoint}.")
                try:
                    print(f"API Response: {response.json()}") # Assuming JSON response
                except requests.exceptions.JSONDecodeError:
                    print(f"API Response (non-JSON): {response.text}")
                return True
            else:
                print(f"Failed to upload file. Status Code: {response.status_code}")
                print(f"API Error Response: {response.text}")
                return False
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during API request: {e}")
        return False
    except IOError as e:
        print(f"Error reading file {filepath}: {e}")
        return False

# Example usage
if __name__ == "__main__":
    # Create a dummy file for testing
    dummy_filepath = os.path.join(settings.OUTPUT_FILE_DIRECTORY, "dummy_upload.txt")
    with open(dummy_filepath, 'w') as f:
        f.write("This is a dummy file for upload testing.")
    print(f"Created dummy file: {dummy_filepath}")

    # Attempt to upload (this will likely fail without a real API endpoint)
    success = upload_file_to_api(dummy_filepath)
    if success:
        print("Dummy file upload test successful (might be a mock server).")
    else:
        print("Dummy file upload test failed (expected if no real API).")

    # Clean up dummy file
    if os.path.exists(dummy_filepath):
        os.remove(dummy_filepath)
        print(f"Removed dummy file: {dummy_filepath}")