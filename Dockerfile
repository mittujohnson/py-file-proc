# 1. Use an official Python runtime as a parent image
# Using a slim version to keep the image size small
FROM python:3.9-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Copy the requirements file and install dependencies
# This is done in a separate step to leverage Docker's layer caching.
# Dependencies will only be re-installed if requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of the application's code into the container
COPY . .

# 5. Set the default command to run when the container starts
# This will execute your main application script.
CMD ["python", "main.py"]