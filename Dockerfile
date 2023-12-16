# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script and requirements files to the working directory
COPY create_users.py .
COPY update_emails.py .
COPY update_aliases.py .
COPY users.csv .
COPY service_account_credentials.json .

# Run the Python script
ENTRYPOINT ["python"]
CMD ["create_users.py"]
