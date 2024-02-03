
from mail_client.get_mail import list_unread_messages


def start():
    # get unread emails
    messages = list_unread_messages()

    if not messages:
        print('No unread messages found.')
    else:
        print('Unread messages:')
        for message in messages:
            print(f"Message ID: {message['id']} - Subject: {message['subject']}")
            print(f"^-- Snippet: {message['snippet']}")
    
    




if __name__ == '__main__':
    start()
