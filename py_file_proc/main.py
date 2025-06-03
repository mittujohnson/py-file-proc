# your_project_name/main.py

import os
from your_project_name.database import db_connector
from your_project_name.file_handler import file_operations
from your_project_name.api_client import api_sender
from your_project_name.config import settings

def run_data_pipeline():
    """
    Orchestrates the data extraction, file creation, and API upload process.
    """
    print("Starting data pipeline...")

    # 1. Define your SQL query to fetch data
    # IMPORTANT: Replace with your actual table and column names
    sql_query = "SELECT user_id, username, email, created_at FROM users WHERE status = 'active';"

    # 2. Fetch data from PostgreSQL
    data = db_connector.fetch_data_from_db(sql_query)

    if not data:
        print("No data fetched from the database. Aborting file creation and upload.")
        return

    # 3. Create a file with the fetched data
    # You can choose to create CSV, JSON, or XML
    output_filename = "active_users_export.xml" # Changed to XML for demonstration
    file_path = file_operations.create_xml_file_from_template(data, output_filename)
    # Uncomment below for other formats if needed:
    # file_path = file_operations.create_csv_file(data, "active_users_export.csv")
    # file_path = file_operations.create_json_file(data, "active_users_export.json")

    if not file_path:
        print("Failed to create the output file. Aborting upload.")
        return

    # 4. Push the created file to the API endpoint
    print(f"Attempting to upload file: {file_path}")
    upload_success = api_sender.upload_file_to_api(file_path)

    if upload_success:
        print("Data pipeline completed successfully: Data fetched, file created, and uploaded.")
        # Optional: Clean up the local file after successful upload
        # os.remove(file_path)
        # print(f"Cleaned up local file: {file_path}")
    else:
        print("Data pipeline completed with errors: File upload failed.")

if __name__ == "__main__":
    run_data_pipeline()