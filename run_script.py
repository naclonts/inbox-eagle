from datetime import datetime
from evaluator.evaluator import MessageEvaluation, evaluate_message_importance
from mail_client.get_mail import list_unread_messages
import commentjson


def start():
    # get unread emails
    messages = list_unread_messages(7, ['INBOX', 'UNREAD'])

    if not messages:
        print('\n\n- No unread messages found -\n\n')
        return

    # Open the config file to get context and settings
    with open('prompt-config-setup.json', 'r') as file:
        prompt_config = commentjson.load(file)

    print(f'\n\n-------- Evaluating messages ({len(messages)}) --------\n')

    evaluations: list[MessageEvaluation]  = []

    for message in messages:
        # Print message headers in green
        print('\033[92m' + f"Message ID: {message['id']} - Subject: {message['subject']}" + '\033[0m')
        print(f"Snippet: {message['snippet']}")

        evaluation = evaluate_message_importance(prompt_config, message)
        print(f'Rating: {evaluation["rating"]}')
        print(f'Evaluation: {evaluation["response"]}')

        print('\n----------------\n')

        evaluations.append(evaluation)

    print('\n\n-------- Finished evaluating messages --------\n')

    # Save evaluations to CSV file
    filename = f'evaluation-results-{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.csv'
    with open(filename, 'w') as file:
        # format MessageEvaluation objects to CSV
        csv = 'Rating,Message Subject,Message Content,Evaluation,Model\n'
        # double quote values to avoid issues with commas
        for evaluation in evaluations:
            csv += f'"{evaluation["rating"]}", "{evaluation["message"]["subject"]}", "{evaluation["response"]}", "{evaluation["model"]}"\n'
        file.write(csv)

    print(f'Evaluation results saved to {filename}')


if __name__ == '__main__':
    start()
