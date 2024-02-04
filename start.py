import json
from evaluator.evaluator import evaluate_message_importance
from mail_client.get_mail import list_unread_messages
import commentjson


def start():
    # get unread emails
    messages = list_unread_messages()

    if not messages:
        print('\n\n- No unread messages found -\n\n')
        return

    # Assuming the settings are stored in settings.json
    with open('prompt-config.json', 'r') as file:
        prompt_config = commentjson.load(file)

    print(f'\n\n-------- Evaluating messages ({len(messages)}) --------\n')
    for message in messages:
        # Print message in green
        print('\033[92m' + f"Message ID: {message['id']} - Subject: {message['subject']}" + '\033[0m')
        print(f"Snippet: {message['snippet']}")
        evaluation = evaluate_message_importance(prompt_config, message)
        print(f'Rating: {evaluation["rating"]}')
        print(f'Evaluation: {evaluation["response"]}')
        print('\n----------------\n')


if __name__ == '__main__':
    start()
