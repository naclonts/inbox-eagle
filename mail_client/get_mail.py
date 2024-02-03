import base64
from distutils import errors
from typing import TypedDict
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import pickle

# The scope tells the script what permissions it has on your Gmail account
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']  # Allows reading and modifying but not deleting emails

def get_gmail_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=33339)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

Message = TypedDict('Message', {
    'body': str,
    'snippet': str,
    'id': str,
    'subject': str
})


def list_unread_messages() -> list[Message]:
    service = get_gmail_service()

    # Fetch unread inbox in the last 20 days
    results = service.users().messages() \
        .list(userId='me', labelIds=['INBOX', 'UNREAD'], q='newer_than:7d') \
        .execute()
    messages = results.get('messages', [])
    
    # return full messages
    return [
        get_mime_message(service, 'me', message['id'])
        for message in messages
    ]


def get_mime_message(service, user_id, msg_id) -> Message:
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        
        # Check if the message is multipart
        payload = message['payload']
        parts = payload.get('parts')
        
        body = ""
        if parts:  # If email has parts, iterate through them
            for part in parts:
                if part['mimeType'] == 'text/plain' or part['mimeType'] == 'text/html':
                    body_data = part['body']['data']
                    body = str(base64.urlsafe_b64decode(body_data), 'utf-8')  # Decode the base64 encoded string
                    break  # Assuming you want the first text/plain or text/html part you encounter
        else:  # Simple email, not multipart
            body_data = payload['body']['data']
            body = str(base64.urlsafe_b64decode(body_data), 'utf-8')
        
        return { 'body': body, 'snippet': message['snippet'], 'id': message['id'], 'subject': message['payload']['headers'][16]['value'] }
    except errors.HttpError as error:
        print(f'An error occurred: {error}')

