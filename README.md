# Google Workspace User Creation Script

This Python script allows you to create users in Google Workspaces using the Google Workspace Admin SDK API.

## Prerequisites

- [Configure Google Admin SDK API and create Service Account](#Configure-Google-Admin-SDK-API-and-create-Service-Account).
    - [Create Organization and Project](#create-organization-and-project)
    - [Enable Admin SDK API](#enable-admin-sdk-api)
    - [Create Service Account and generate credentials](#create-service-account-and-generate-credentials)
    - [Assign a role to a service account](#assign-a-role-to-a-service-account)


- Prepare a CSV file (users.csv) containing the user data. The CSV file should have the following columns:
    ```
    first_name: First name of the user.
    last_name: Last name of the user.
    password: Password for the user.
    username (optional): Desired username for the user. If not provided, a default username will be generated based on the first name and last name.
    ```
    Example CSV file:

    ```csv

    first_name,last_name,password,username
    John,Doe,pass123,
    Jane,Smith,secure321,janesmith
    Adam,Johnson,abc123,
    ```
- Place the `service_account_credentials.json` and `users.csv` files in the same directory as the script.

## Usage

1. Build the Docker image by running the following command in the terminal:

    ```bash
    docker build -t user-creation .
    ```

2. Run the Docker container using the following command:

    ```bash
    docker run --rm -e DOMAIN=example.com -it user-creation
    ```

## Configure Google Admin SDK API and create Service Account


### Create Organization and Project

1. Sign in to the [Google Cloud Console](https://console.cloud.google.com).
2. If you don't have an organization, you will be prompted to create one. Click on the "Get started" button to proceed. If you already have an organization, skip to step 6.
3. Fill in the required information for your organization, including the organization name, display name, and the primary domain name for your organization's email addresses. Click on the "Create" button to create the organization.
4. Read and accept the terms of service for Google Cloud.
5. Set up your organization's billing account by providing the necessary information and selecting a billing plan. This step is required to enable Google Cloud services and create projects.
6. With your organization created, you can now create a project. In the Google Cloud Console, click on the project dropdown menu in the top navigation bar and select "New Project".
7. Enter a name for your project and select the organization you created in the previous steps from the dropdown menu.
8. Optionally, you can specify a project ID or let Google Cloud generate one for you. The project ID must be unique within Google Cloud and can contain lowercase letters, digits, and hyphens.
9. Click on the "Create" button to create the project.

### Enable Admin SDK API

- Go to https://console.developers.google.com/apis/api/admin.googleapis.com/ 
- Click Enable


### Create Service Account and generate credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com).
2. Create a new project or select an existing project.
3. In the sidebar, click on "IAM & Admin" and then select "Service Accounts".
4. Click on the "Create Service Account" button.
5. Enter a name for the service account and provide an optional description. Then click on the "Create" button.
6. In the "Service account permissions" step, you can grant the necessary permissions to the service account based on your requirements. For accessing Google Workspace Admin SDK, you need to grant the "Service Account Admin" role.
7. In the next step, you can add any optional users to grant access to the service account. If you don't have any specific users to add, you can skip this step.
8. Click on the "Create Key" button.
9. Select the key type as "JSON" and click on the "Create" button. This will download the service account credentials JSON file to your computer.

After following these steps, you will have the service account credentials JSON file (service_account_credentials.json) that you can use in the Python script to authenticate and authorize access to the Google Workspace Admin SDK.

### Assign a role to a service account

1. In the [Google Admin console](https://admin.google.com), go to Menu menu> Account > Admin roles.
2. Point to the role **User Management Administrator**, and then click Assign admin.
3. Click Assign service accounts.
4. Enter the email address of the service account. (From service_account_credentials.json)
5. Click Add > Assign role.
