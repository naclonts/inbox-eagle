
from evaluator.evaluator import get_important_messages
from mail_client.get_mail import list_unread_messages


def start():
    # get unread emails
    messages = list_unread_messages()

    if not messages:
        print('No unread messages found.')
    else:
        print(f'-------- All unread messages ({len(messages)}) --------')
        for message in messages:
            print(f"Message ID: {message['id']} - Subject: {message['subject']}")
            print(f"^-- Snippet: {message['snippet']}")
    

    # Determine which ones are important to respond to
    important_messages = get_important_messages(messages)
    print(important_messages)




if __name__ == '__main__':
    start()
