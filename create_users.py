import csv
import time
import os
import signal
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to your service account credentials JSON file
SERVICE_ACCOUNT_FILE = 'service_account_credentials.json'

# Scopes required for accessing the Admin SDK
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']

# ID of the Google Workspace domain
DOMAIN = os.environ.get('DOMAIN')

# Check if DOMAIN environment variable is set
if DOMAIN is None:
    raise ValueError("DOMAIN environment variable is not set.")

# Function to create a new user
def create_user(user_data):
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build('admin', 'directory_v1', credentials=credentials)

    first_name = user_data['first_name']
    last_name = user_data['last_name']
    password = user_data['password']
    username = user_data['username']

    # If username is empty, assign a default value
    if not username:
        username = f'{first_name.lower()}.{last_name.lower()}'

    # sleep 2 seconds to avoid 412 limits (NOTE: 10 and 20 users limit for fresh Google Workspace Accounts )
    time.sleep(2)

    print(f'\nCreating user: {username}')

    # Construct the user object
    user = {
        'name': {
            'givenName': first_name,
            'familyName': last_name
        },
        'primaryEmail': f'{username}@{DOMAIN}',
        'password': password,
        'changePasswordAtNextLogin': True
    }

    try:
        # Create the user
        created_user = service.users().insert(body=user).execute()
        print(f'Successfully created user: {created_user["primaryEmail"]}')
    except Exception as e:
        if e.resp.status == 409:
            print(f'User with email {user["primaryEmail"]} already exists')
        else:
            print(f'Error creating user: {str(e)}')

# Load user data from CSV file
def load_user_data(file_path):
    user_data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_data.append(row)
    return user_data

# Define a cleanup function to be called on keyboard interrupt
def cleanup(signal, frame):
    print("Keyboard interrupt received. Exiting...")
    sys.exit(0)

# Register the cleanup function for SIGINT signal (Ctrl-C)
signal.signal(signal.SIGINT, cleanup)

# Example usage
user_data = load_user_data('users.csv')
for user in user_data:
    create_user(user)
