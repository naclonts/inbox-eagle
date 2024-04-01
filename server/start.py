from flask import Flask, jsonify, request
from flask_cors import CORS

from evaluator.evaluator import evaluate_message_importance
from evaluator.types import MessageEvaluation
from mail_client.get_mail import get_unread_messages
from server.utils import load_prompt_config, log_evaluation

app = Flask(__name__)
CORS(app)

@app.route('/get-email-evaluations', methods=['POST'])
def get_email_evaluations():
    request_data = request.get_json()
    num_days_to_include = request_data.get('numDaysToInclude', 3)
    email_type_filter = request_data.get('emailTypeFilter', ['INBOX', 'UNREAD'])

    # Fetch the unread messages from Gmail
    messages = get_unread_messages(num_days_to_include, email_type_filter)

    # For each message, evaluate its importance with the LLM
    evaluations: list[MessageEvaluation] = []
    prompt_config = load_prompt_config()
    for message in messages:
        evaluation = evaluate_message_importance(prompt_config, message)
        evaluations.append(evaluation)
        log_evaluation(message, evaluation)

    # Sort evaluations to show the most important messages first
    sorted_evaluations = sorted(evaluations, key=lambda x: x['rating'], reverse=True)

    # Return the messages and ratings to the front-end
    return jsonify({
        'evaluations': [
            {
                "rating": eval['rating'],
                "from": eval['message']['from'],
                "subject": eval['message']['subject'],
                "snippet": eval['message']['snippet'],
                "evaluatorResponse": eval['response'],
                "model": eval['model'],
                "receivedAt": eval['message']['receivedAt']
            } for eval in sorted_evaluations
        ]
    })


def start_server():
    app.run(debug=True, port=5020)

