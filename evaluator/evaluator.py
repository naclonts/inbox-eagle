from dotenv import load_dotenv
import os
from evaluator import prompt_writer
import openai
from mailbox import Message
import requests

load_dotenv('.environment')

EVALUATOR_MODEL = 'gpt-3.5-turbo'
openai.api_key = os.environ['OPENAI_API_KEY']


headers = {
    "Content-Type": "application/json"
}


def evaluate_message_importance(prompt_config, message: Message) -> str:
    # limit the message to the first and last 2000 characters
    trimmed_content = message['body'][:2000] + '\n...\n' + message['body'][-2000:]
    prompt = prompt_writer.get_message_evaluation_prompt(prompt_config, trimmed_content)

    if EVALUATOR_MODEL == 'local':
        return get_local_llm_response(prompt)

    elif EVALUATOR_MODEL[0:3] == 'gpt':
        return get_chatgpt_response(prompt)

    raise ValueError('Invalid Evaluator model')


def get_local_llm_response(prompt):
    response = requests.post(
        'http://localhost:5000/v1/chat/completions',
        headers=headers,
        json={
            "mode": "instruct",
            "instruction_template": "Alpaca", # not sure what this does...
            "messages": prompt,
        },
    )
    assistant_message = response.json()['choices'][0]['message']['content']
    return assistant_message

def get_chatgpt_response(prompt):
    client = openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    chat_completion = client.chat.completions.create(
        messages=prompt,
        model=EVALUATOR_MODEL,
    )
    return chat_completion
