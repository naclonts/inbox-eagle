import json
from evaluator.evaluator import evaluate_message_importance
from mail_client.get_mail import list_unread_messages


def start():
    # get unread emails
    messages = list_unread_messages()

    if not messages:
        print('\n\n- No unread messages found -\n\n')
        return



    # Assuming the settings are stored in settings.json
    with open('prompt-config.json', 'r') as file:
        prompt_config = json.load(file)

    print(f'-------- All unread messages ({len(messages)}) --------')
    for message in messages:
        print(f"Message ID: {message['id']} - Subject: {message['subject']}")
        print(f"^-- Snippet: {message['snippet']}")
        evaluation = evaluate_message_importance(prompt_config, message)
        print(evaluation)
        print('\n----------------\n')




if __name__ == '__main__':
    start()
