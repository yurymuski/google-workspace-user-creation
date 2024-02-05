import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the scope for Google Workspace Admin SDK API
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']

# Path to the service account key file (JSON)
SERVICE_ACCOUNT_FILE = 'service_account_credentials.json'

# ID of the Google Workspace domain
DOMAIN = os.environ.get('DOMAIN')

# Check if DOMAIN environment variable is set
if DOMAIN is None:
    raise ValueError("DOMAIN environment variable is not set.")

# Function to authenticate and get the service object
def authenticate_google_workspace():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Build the Google Workspace Admin SDK API service
    service = build('admin', 'directory_v1', credentials=credentials)
    return service

# Function to get a list of users with a domain filter
def get_user_list(service):
    users = service.users().list(domain=DOMAIN, orderBy='email').execute()
    return users.get('users', [])

# Function to suspend a user
def suspend_user(service, user_id):
    try:
        service.users().update(
            userKey=user_id,
            body={'suspended': True}
        ).execute()
        print(f"User {user_id} suspended successfully.")
    except HttpError as e:
        error_message = e.content.decode('utf-8')
        print(f"Error suspending user {user_id}: {error_message}")

def main():
    # Authenticate and get the service object
    service = authenticate_google_workspace()

    # Get the list of users from the specified domain
    users = get_user_list(service)

    # Suspend all users from the list
    for user in users:
        print(user['primaryEmail'])
        suspend_user(service, user['id'])

    print("Users from the domain {} suspended successfully.".format(DOMAIN))

if __name__ == '__main__':
    main()
