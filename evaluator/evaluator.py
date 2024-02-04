import re
from typing import TypedDict
from dotenv import load_dotenv
import os
from evaluator import prompt_writer
import openai
from mailbox import Message
import requests

load_dotenv('.environment')

openai.api_key = os.environ['OPENAI_API_KEY']


headers = {
    "Content-Type": "application/json"
}


# define a typed MessageEvaluation object
MessageEvaluation = TypedDict('MessageEvaluation', {
    'message': Message,
    'rating': float,
    'evaluation': str,
    'model': str,
})


def evaluate_message_importance(prompt_config, message: Message) -> MessageEvaluation:
    # limit the message to the first and last 2000 characters
    trimmed_content = message['body'][:2000] + '\n...\n' + message['body'][-2000:]
    prompt = prompt_writer.get_message_evaluation_prompt(prompt_config, trimmed_content)

    if prompt_config['evaluator_model'] == 'local':
        completion = get_local_llm_response(prompt_config, prompt)

    elif prompt_config['evaluator_model'][0:3] == 'gpt':
        completion = get_chatgpt_response(prompt_config, prompt)

    else:
        raise ValueError('Invalid Evaluator model ' + prompt_config['evaluator_model'])

    response = completion['choices'][0]['message']['content'].strip()
    try:
        rating = float(re.sub('\s+', '', response.split('Importance Level: ')[1]))
    except Exception as e:
        print('Error parsing response for rating: ', e)
        rating = -1

    return MessageEvaluation(
        message=message,
        rating=rating,
        response=response,
        model=prompt_config['evaluator_model'],
    )


def get_local_llm_response(prompt_config, prompt):
    response = requests.post(
        'http://localhost:5000/v1/chat/completions',
        headers=headers,
        json={
            "mode": "instruct",
            "instruction_template": "Alpaca", # not sure what this does...
            "messages": prompt,
        },
    )
    assistant_message = response.json()
    return assistant_message

def get_chatgpt_response(prompt_config, prompt):
    client = openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    chat_completion = client.chat.completions.create(
        messages=prompt,
        model=prompt_config['evaluator_model'],
    )
    return chat_completion
