import commentjson
from flask import Flask, jsonify, request
from flask_cors import CORS
from evaluator.evaluator import evaluate_message_importance
from evaluator.types import MessageEvaluation

from mail_client.get_mail import list_unread_messages

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/get-email-evaluations', methods=['POST'])
def get_email_evaluations():
    data = request.get_json()

    # Extracting values from the JSON object
    # TODO: use these parameters!
    num_days_to_include = data.get('numDaysToInclude', 3)
    email_type_filter = data.get('emailTypeFilter', ['INBOX', 'UNREAD'])

    # get unread emails
    messages = list_unread_messages(num_days_to_include, email_type_filter)

    if not messages:
        print('\n\n- No unread messages found -\n\n')
        return jsonify({
            'evaluations': []
        })

    # Open the config file to get context and settings
    with open('prompt-config.json', 'r') as file:
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

    response = jsonify({
        'evaluations': [
            {
                "rating": eval['rating'],
                "subject": eval['message']['subject'],
                "snippet": eval['message']['snippet'],
                "evaluatorResponse": eval['response'],
                "model": eval['model'],
                "receivedAt": eval['message']['receivedAt']
            } for eval in evaluations
        ]
    })
    return response


def start_server():
    app.run(debug=True, port=5020)

