import re
from evaluator import prompt_writer
from mail_client.get_mail import Message
from evaluator.extract_evaluator_rating import extract_rating_from_evaluation
from evaluator.types import MessageEvaluation

from llm_api.api import get_llm_response


def evaluate_message_importance(prompt_config, message: Message) -> MessageEvaluation:
    # limit the message to the first and last 2000 characters
    trimmed_content = message['body'][:2000] + '\n...\n' + message['body'][-2000:] + '\n...\nSnippet: ' + message['snippet']
    prompt = prompt_writer.get_message_evaluation_prompt(prompt_config, trimmed_content)

    response = get_llm_response(prompt_config, prompt)

    rating = extract_rating_from_evaluation(prompt_config, response)

    return MessageEvaluation(
        message=message,
        rating=rating,
        response=response,
        model=prompt_config['evaluator_model'],
    )


