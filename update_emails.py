import httplib2
import apiclient.discovery
from google.oauth2 import service_account

# Set the credentials for the service account with necessary permissions
credentials = service_account.Credentials.from_service_account_file(
    './service_account_credentials.json',
    scopes=['https://www.googleapis.com/auth/admin.directory.user', 'https://www.googleapis.com/auth/admin.directory.group']
)

# Create an authorized API client
service = apiclient.discovery.build('admin', 'directory_v1', credentials=credentials)

def update_user_domain(user_key, new_domain, processed_users):
    try:
        if user_key in processed_users:
            print(f"User {user_key} already updated. Skipping.")
            return

        # Get the current user details
        user = service.users().get(userKey=user_key).execute()

        # Extract the username from the current email
        username, _ = user['primaryEmail'].split('@')

        # Update the email address with the new domain
        user['primaryEmail'] = f"{username}@{new_domain}"

        # Update the user with the new email
        updated_user = service.users().update(userKey=user_key, body=user).execute()

        print(f"Updated domain for user {username}. New email: {user['primaryEmail']}")

        # Add the user to the list of processed users
        processed_users.add(user_key)

    except apiclient.errors.HttpError as e:
        error_message = e.content.decode('utf-8') if e.content else str(e)
        print(f"{username}")
        print(f"HttpError: {error_message}")
    except Exception as e:
        print(f"Error updating domain for user {user_key}: {str(e)}")

def update_group_domain(group_email, new_domain, processed_groups):
    try:
        if group_email in processed_groups:
            print(f"Group {group_email} already updated. Skipping.")
            return

        # Get the current group details
        group = service.groups().get(groupKey=group_email).execute()

        # Update the email address with the new domain
        group['email'] = f"{group_email.split('@')[0]}@{new_domain}"

        # Update the group with the new email
        updated_group = service.groups().update(groupKey=group_email, body=group).execute()

        print(f"Updated domain for group {group_email}. New email: {group['email']}")

        # Add the group to the list of processed groups
        processed_groups.add(group_email)

    except apiclient.errors.HttpError as e:
        error_message = e.content.decode('utf-8') if e.content else str(e)
        print(f"HttpError: {error_message}")
    except Exception as e:
        print(f"Error updating domain for group {group_email}: {str(e)}")

def main():
    try:
        # List all users in the domain
        users = service.users().list(domain='example.net').execute()

        # Specify the new domain
        new_domain = 'example.com'

        # Keep track of processed users and groups
        processed_users = set()
        processed_groups = set()

        # Check if there are users in the domain
        if 'users' in users:
            # Iterate through each user and update their email address
            for user in users['users']:
                # Update the user's email address with the new domain
                update_user_domain(user['id'], new_domain, processed_users)
        else:
            print("No users found in the domain.")

        # List all groups in the domain
        groups = service.groups().list(domain='example.net').execute()

        # Check if there are groups in the domain
        if 'groups' in groups:
            # Iterate through each group and update their email address
            for group in groups['groups']:
                # Update the group's email address with the new domain
                update_group_domain(group['email'], new_domain, processed_groups)
        else:
            print("No groups found in the domain.")

    except apiclient.errors.HttpError as e:
        error_message = e.content.decode('utf-8') if e.content else str(e)
        print(f"HttpError: {error_message}")
    except Exception as e:
        print(f"Error processing users and groups: {str(e)}")

if __name__ == '__main__':
    main()
