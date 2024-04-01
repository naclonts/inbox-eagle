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
    """Returns the Gmail API service, while caching the tokens to a pickle file."""
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
                'credentials-gmail.json', SCOPES)
            creds = flow.run_local_server(port=33339)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

Message = TypedDict('Message', {
    'body': str,
    'from': str,
    'snippet': str,
    'id': str,
    'subject': str,
    'receivedAt': str
})


def get_unread_messages(num_days_to_include: int, email_type_filter: list[str]) -> list[Message]:
    """Returns unread messages from Gmail that were received within the last N days."""
    service = get_gmail_service()

    # Fetch unread inbox in the last N days
    results = service.users().messages() \
        .list(userId='me', labelIds=email_type_filter, q=f'newer_than:{num_days_to_include}d') \
        .execute()
    messages = results.get('messages', [])

    # return full messages
    return [
        get_decoded_message(service, 'me', message['id'])
        for message in messages
    ]


def get_decoded_message(service, user_id, msg_id) -> Message:
    """
    Given a message ID, this returns a text version of the message.

    Note that this function currently doesn't always handle threads correctly -- could
    use some improvements here!
    """
    message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()

    # Check if the message is multipart
    payload = message['payload']
    headers = payload['headers']
    parts = payload.get('parts')
    subject = [i['value'] for i in headers if i["name"]=="Subject"]

    body = ""
    if parts:  # If email has parts, iterate through them
        for part in parts:
            if part['mimeType'] == 'text/plain' or part['mimeType'] == 'text/html':
                body_data = part['body'].get('data', '')
                body = str(base64.urlsafe_b64decode(body_data), 'utf-8')  # Decode the base64 encoded string
                subject= [i['value'] for i in headers if i["name"]=="Subject"]
                break  # Assuming you want the first text/plain or text/html part you encounter


        # handle parts nested within parts

    else:  # Simple email, not multipart
        body_data = payload['body'].get('data', '')
        body = str(base64.urlsafe_b64decode(body_data), 'utf-8')

    return {
        'body': body,
        'snippet': message['snippet'],
        'from': [i['value'] for i in headers if i["name"]=="From"][0],
        'id': message['id'],
        'subject': subject or '',
        'receivedAt': message['internalDate']
    }

