from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def remove_matching_aliases(service, email, aliases, is_user):
    """
    Remove aliases where the first part matches the email's first part.
    """
    first_part_email = email.split('@')[0]
    matching_aliases = [alias for alias in aliases if alias.split('@')[0] == first_part_email]

    for alias in matching_aliases:
        try:
            print(f"Removing alias {alias} for {email}")
            if is_user:
                # Remove alias from user
                service.users().aliases().delete(userKey=email, alias=alias).execute()
            else:
                # Remove alias from group
                service.groups().aliases().delete(groupKey=email, alias=alias).execute()
        except HttpError as e:
            # Catch HttpError and print the error message
            print(f"Error removing alias {alias} for {email}: {e.content}")

def get_user_aliases(service, domain):
    try:
        # Display aliases for each user
        users_request = service.users().list(domain=domain, maxResults=200).execute()

        users = users_request.get('users', [])

        for user in users:
            user_email = user['primaryEmail']
            try:
                response = service.users().get(userKey=user_email).execute()
                aliases = response.get('aliases', [])

                # Remove aliases where the first part matches the user's first part of the email
                remove_matching_aliases(service, user_email, aliases, is_user=True)

                print(f"Aliases for user {user_email}: {aliases}")

            except HttpError as e:
                # Catch HttpError and print the error message
                print(f"Error getting aliases for user {user_email}: {e.content}")

    except Exception as e:
        print(f"An error occurred: {e}")

def get_group_aliases(service, domain):
    try:
        # Display aliases for each group
        response = service.groups().list(domain=domain).execute()
        groups = response.get('groups', [])

        for group in groups:
            group_email = group['email']
            try:
                response = service.groups().get(groupKey=group_email).execute()
                aliases = response.get('aliases', [])

                # Remove aliases where the first part matches the group's first part of the email
                remove_matching_aliases(service, group_email, aliases, is_user=False)

                print(f"Aliases for group {group_email}: {aliases}")

            except HttpError as e:
                # Catch HttpError and print the error message
                print(f"Error getting aliases for group {group_email}: {e.content}")

    except Exception as e:
        print(f"An error occurred: {e}")

def update_user_aliases(service, domain, previos_domain):
    try:
        # Display aliases for each user
        users_request = service.users().list(domain=domain).execute()

        users = users_request.get('users', [])
        print(f"{len(users)}")
        for user in users:
            user_email = user['primaryEmail']
            print(f"Checking {user_email}")
            try:
                response = service.users().get(userKey=user_email).execute()
                current_aliases = response.get('aliases', [])
                aliases_with_previous_domain = [alias for alias in current_aliases if previos_domain in alias]

                for alias in aliases_with_previous_domain:
                    try:
                        updated_alias=f"{alias.split('@')[0]}@{domain}"

                        print(f"Adding alias {updated_alias} for {user_email}")
                        # Adding alias from user
                        service.users().aliases().insert(userKey=user_email, body={'alias': updated_alias}).execute()

                        print(f"Removing alias {alias} for {user_email}")
                        # Remove alias from user
                        service.users().aliases().delete(userKey=user_email, alias=alias).execute()

                    except HttpError as e:
                        # Check if it's a Not Authorized error
                        if e.resp.status == 403:
                            print(f"Not authorized to access this resource/api: {e.content}")
                        else:
                            # Print the error for other cases
                            print(f"Error updating alias {alias} for {user_email}: {e.content}")

            except HttpError as e:
                # Check if it's a Not Authorized error
                if e.resp.status == 403:
                    print(f"Not authorized to access this resource/api: {e.content}")
                else:
                    # Print the error for other cases
                    print(f"Error updating alias {alias} for {user_email}: {e.content}")


    except HttpError as e:
        # Catch HttpError and print the error message
        print(f"Error getting aliases for user {user_email}: {e.content}")

# Replace 'path/to/your/credentials.json' and 'yourdomain.com' with your actual values
credentials_file = './service_account_credentials.json'
domain = 'example.com'
previos_domain = 'example.net'

# Set the scope for the Admin SDK
scope = ['https://www.googleapis.com/auth/admin.directory.user', 'https://www.googleapis.com/auth/admin.directory.group']

# Create credentials using the service account JSON file and specified scope
credentials = service_account.Credentials.from_service_account_file(credentials_file, scopes=scope)

# Create the Admin SDK service
service = build('admin', 'directory_v1', credentials=credentials)

# Update and display user aliases with the new domain
update_user_aliases(service, domain, previos_domain)

# Get and display user aliases
get_user_aliases(service, domain)

# Get and display group aliases
get_group_aliases(service, domain)


